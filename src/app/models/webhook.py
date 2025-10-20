from sqlalchemy import Column, String, JSON, DateTime, func, Boolean
from app.core.database import Base

class WebhookEvent(Base):
    __tablename__ = "webhooks"

    id = Column(String, primary_key=True)
    event = Column(String)
    payload = Column(JSON)
    processed = Column(Boolean, default=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
