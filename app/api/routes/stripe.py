from fastapi import APIRouter, Request, HTTPException, Depends
import stripe
from app.core.config import get_settings
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.api.deps import get_current_user, require_active_subscription
from datetime import datetime
from app.models.webhook_event import WebhookEvent

router = APIRouter(prefix="/stripe", tags=["stripe"])

def log(msg):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")


settings = get_settings()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook payload")

    event_id = event["id"]
    event_type = event["type"]

    exists = db.query(WebhookEvent).filter(
        WebhookEvent.event_id == event_id
    ).first()

    if exists:
        log(f"⚠️ duplicate webhook ignored: {event_id}")
        return {"status": "ignored"}

    log(f"📩 event type: {event_type}")

    # -----------------------------
    # checkout.session.completed
    # -----------------------------
    if event_type == "checkout.session.completed":

        session = event["data"]["object"]

        email = session.get("metadata", {}).get("email")

        if not email:
            log("⚠️ email metadata missing")
            return {"status": "ignored"}

        user = db.query(User).filter(User.email == email).first()

        if not user:
            log("⚠️ user not found")
            return {"status": "ignored"}

        subscription_id = session.get("subscription")
        customer_id = session.get("customer")

        if not subscription_id or not customer_id:
            log("⚠️ missing required subscription data")
            return {"status": "ignored"}

        subscription = stripe.Subscription.retrieve(
            subscription_id,
            expand=["latest_invoice", "latest_invoice.lines"]
        )

        period_end_ts = subscription.get("current_period_end")

        if not period_end_ts:
            latest = subscription.get("latest_invoice")
            lines = latest.get("lines", {}).get("data", []) if latest else []

            if lines:
                period_end_ts = lines[0].get("period", {}).get("end")

        if not period_end_ts:
            log("⚠️ period_end not found")
            return {"status": "ignored"}

        period_end = datetime.utcfromtimestamp(period_end_ts)

        user = db.query(User).filter(
            User.stripe_customer_id == customer_id
        ).first()

        if not user:
            log("⚠️ user not found")
            return {"status": "ignored"}

        user.subscription_status = "PRO"
        user.current_period_end = period_end
        db.commit()

        log(f"🔥 PRO化: {user.email} {period_end}")
        db.add(WebhookEvent(event_id=event_id))
        db.commit()

        return {"status": "ok"}

    # -----------------------------
    # subscription updated
    # -----------------------------
    elif event_type == "customer.subscription.updated":

        subscription = event["data"]["object"]

        customer_id = subscription.get("customer")

        items = subscription.get("items", {}).get("data", [])

        if not items:
            log("⚠️ subscription update missing items")
            return {"status": "ignored"}

        period_end_ts = items[0].get("current_period_end")

        if not period_end_ts:
            return {"status": "ignored"}

        period_end = datetime.utcfromtimestamp(period_end_ts)

        user = db.query(User).filter(
            User.stripe_customer_id == customer_id
        ).first()

        if not user:
            return {"status": "ignored"}

        user.current_period_end = period_end
        db.commit()

        log(f"🔄 subscription updated: {user.email}")

        return {"status": "ok"}

    # -----------------------------
    # payment failed
    # -----------------------------
    elif event_type == "invoice.payment_failed":

        invoice = event["data"]["object"]
        customer_id = invoice.get("customer")

        user = db.query(User).filter(
            User.stripe_customer_id == customer_id
        ).first()

        if user:
            user.subscription_status = "CANCELED"
            db.commit()
            log(f"⚠️ payment failed: {user.email}")

        return {"status": "ok"}

    # -----------------------------
    # subscription deleted
    # -----------------------------
    elif event_type == "customer.subscription.deleted":

        subscription = event["data"]["object"]
        customer_id = subscription.get("customer")

        user = db.query(User).filter(
            User.stripe_customer_id == customer_id
        ).first()

        if user:
            user.subscription_status = "CANCELED"
            user.current_period_end = datetime.utcnow()
            db.commit()

            log(f"🗑 subscription deleted: {user.email}")

        return {"status": "ok"}

    return {"status": "ignored"}
    

@router.post("/create-checkout-session")
def create_checkout_session(
    current_user: User = Depends(get_current_user),
):
    session = stripe.checkout.Session.create(
        customer=current_user.stripe_customer_id,
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": settings.STRIPE_PRICE_ID,
            "quantity": 1,
        }],
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
        metadata={
            "email": current_user.email
        }
    )

    return{"url": session.url}


@router.get("/pro-content")
def pro_content(
    current_user: User = Depends(require_active_subscription),
):
    return{"message": "🔥 PROユーザー専用コンテンツ"}


@router.get("/me")
def read_me(
    current_user: User = Depends(get_current_user),
):
    return{
        "id": current_user.id,
        "email": current_user.email,
        "subscription_status": current_user.subscription_status,
        "current_period_end": current_user.current_period_end,
    }

@router.get("/success")
def stripe_success():
    return {"message": "Payment successful"}