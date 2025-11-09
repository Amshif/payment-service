from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payments_service import PaymentService
from app.schemas.refunds import RefundCreate, RefundResponse

router = APIRouter(prefix="/payments", tags=["Refunds"])

@router.post("/{payment_id}/refund", response_model=RefundResponse)
def create_refund(payment_id: str, payload: RefundCreate, db: Session = Depends(get_db)):
    service = PaymentService(db)
    refund = service.create_refund(payment_id, amount=payload.amount, reason=payload.reason)
    return refund
