from sqlalchemy import Column, String, ForeignKey, Numeric, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
import enum

class OrderStatus(str, enum.Enum):
    created = "created"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    razorpay_order_id = Column(String, unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="INR")
    status = Column(Enum(OrderStatus), default=OrderStatus.created)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
