from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
import enum

class PaymentStatus(str, enum.Enum):
    created = "created"
    captured = "captured"
    failed = "failed"
    refunded = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    razorpay_payment_id = Column(String, unique=True)
    amount = Column(Numeric(10, 2))
    method = Column(String)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.created)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
