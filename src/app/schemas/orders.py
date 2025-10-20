from pydantic import BaseModel, Field
from uuid import UUID

class OrderCreateRequest(BaseModel):
    amount: float
    currency: str = "INR"

class OrderResponse(BaseModel):
    id: UUID
    razorpay_order_id: str
    amount: float
    currency: str
    status: str
