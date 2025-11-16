from sqlalchemy import Column, String, Boolean, DateTime, JSON, text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.core.database import Base


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_id = Column(String(128), unique=True, nullable=False)
    event_type = Column(String(128), nullable=False)
    payload = Column(JSON, nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=text("now()"))
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    processing_error = Column(String)
