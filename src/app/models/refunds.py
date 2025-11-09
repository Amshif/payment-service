import uuid
from sqlalchemy import (Column,String,BigInteger,Text,DateTime,Enum,JSON,ForeignKey,func,)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum as PyEnum


class RefundStatus(str, PyEnum):
    created = "created"
    processed = "processed"
    failed = "failed"


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_id = Column(UUID(as_uuid=True),ForeignKey("payments.id", ondelete="CASCADE"),nullable=False,index=True,)
    razorpay_refund_id = Column(String(128), unique=True)
    amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="INR")
    status = Column(Enum(RefundStatus), default=RefundStatus.created, nullable=False)
    reason = Column(Text, nullable=True)
    failure_reason = Column(Text, nullable=True)
    refund_metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    # payment = relationship("Payment", back_populates="refunds")
