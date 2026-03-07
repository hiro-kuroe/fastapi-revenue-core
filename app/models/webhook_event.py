from sqlalchemy import Column, Integer, String
from app.db import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True)
    event_id = Column(String, unique=True, nullable=False)