from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import get_settings
from datetime import timedelta, datetime, timezone
from app.core.security import create_access_token, decode_access_token
from app.db import engine, Base, get_db
from app.models import user, webhook_event
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.hashing import get_password_hash, verify_password
from app.api.deps import get_current_user, require_active_subscription
from app.models.enums import SubscriptionStatus
from app.api.routes import stripe


settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(stripe.router)


@app.get("/")
def root():
    return{
        "app": settings.APP_NAME,
        "env": settings.ENV,
    }

@app.post("/token", summary="Login (username = email)")
def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=30),
    )

    return{"access_token": access_token, "token_type": "bearer"}


@app.get("/verify")
def verify_token(token: str):
    payload = decode_access_token(token)
    return{"payload": payload}

@app.get("/protected")
def protected_route(current_user: User = Depends(require_active_subscription)):
    return{
        "message": "Protected access granted",
        "user_id": current_user.id,
        "email": current_user.email,
    }


@app.post("/users")
def create_user(email: str, password: str, db: Session = Depends(get_db)):
    user = User(
        email=email,
        hashed_password=get_password_hash(password), 
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return{"id": user.id, "email": user.email}


@app.post("/admin/upgrade/{user_id}")
def upgrade_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.subscription_status = SubscriptionStatus.PRO
    db.commit()
    db.refresh(user)

    return{"message": "User upgraded", "status": user.subscription_status}

@app.get("/free-area")
def free_area(current_user: User = Depends(get_current_user)):
    return{"message": "Everyone logged-in can access this"}

@app.get("/pro-area")
def pro_area(current_user: User = Depends(require_active_subscription)):
    return{"message": "Active subscription users here"}

@app.post("/admin/cancel/{user_id}")
def cancel_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.subscription_status = SubscriptionStatus.CANCELED
    db.commit()
    db.refresh(user)

    return{
        "message": "User canceled",
        "status": user.subscription_status
    }

@app.post("/admin/grant/{user_id}")
def grant_subscription(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    now = datetime.now(timezone.utc)
    user.current_period_end = now + timedelta(days=days)
    user.subscription_status = SubscriptionStatus.PRO

    db.commit()
    db.refresh(user)

    return{
        "message": f"Granted {days} days",
        "current_period_end": user.current_period_end,
        "status": user.subscription_status,
    }