from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from app.db import Base
from app.models.enums import SubscriptionStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    subscription_status = Column(
        SAEnum(SubscriptionStatus),
        nullable=False,
        default=SubscriptionStatus.FREE
    )

    stripe_customer_id = Column(
        String,
        nullable=True)
    
    stripe_subscription_id = Column(
        String,
        nullable=True
    )

    current_period_end = Column(DateTime, nullable=True)



