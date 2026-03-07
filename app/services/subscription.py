from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.enums import SubscriptionStatus


def ensure_active_subscription(user: User, db: Session) -> bool:
    now = datetime.utcnow()

    if(
        user.subscription_status == SubscriptionStatus.PRO
        and user.current_period_end is not None
        and user.current_period_end <= now
    ):
        user.subscription_status = SubscriptionStatus.EXPIRED
        db.commit()

    return user.subscription_status == SubscriptionStatus.PRO