from sqlalchemy import Column, String, Enum, Boolean, JSON, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum

class PaymentStatus(str, enum.Enum):
    created = "created"
    authorized = "authorized"
    captured = "captured"
    failed = "failed"
    refunded = "refunded"
    disputed = "disputed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False)
    razorpay_payment_id = Column(String(128), unique=True)
    payment_gateway = Column(String(50), default="razorpay")
    amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="INR")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.created)
    method = Column(String(30))
    method_details = Column(JSON, default={})
    capture = Column(Boolean, default=True)
    captured_at = Column(DateTime)
    payment_metadata = Column(JSON, default={})
    idempotency_key = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
