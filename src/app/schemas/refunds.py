from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class RefundCreate(BaseModel):
    amount: int | None = None
    reason: str | None = None

class RefundResponse(BaseModel):
    id: UUID
    payment_id: UUID
    razorpay_refund_id: str
    amount: int
    currency: str
    status: str
    reason: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
