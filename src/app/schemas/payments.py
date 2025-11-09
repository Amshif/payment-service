from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class PaymentCreate(BaseModel):
    order_id: UUID
    amount: int = Field(..., gt=0)
    currency: str = Field(default="INR", max_length=3)
    capture: bool = True

class PaymentResponse(BaseModel):
    id: UUID
    razorpay_payment_id: Optional[str] = None
    payment_gateway: str
    amount: int
    currency: str
    status: str
    capture: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaymentStatusUpdate(BaseModel):
    status: str
