from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base


class ProcessedStripeEvent(Base):
    __tablename__ = "processed_stripe_events"

    id = Column(Integer, primary_key=True, index=True)

    stripe_event_id = Column(String, unique=True, index=True, nullable=False)

    event_type = Column(String, nullable=False)

    processed_at = Column(DateTime, nullable=False, default=datetime.utcnow)