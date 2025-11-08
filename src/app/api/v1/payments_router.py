from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payments_service import PaymentService
from app.schemas.payments import PaymentCreate, PaymentResponse, PaymentStatusUpdate

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    service = PaymentService(db)
    payment = service.create_payment(payload)
    return payment


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.patch("/{payment_id}/status", response_model=PaymentResponse)
def update_payment_status(
    payment_id: str, payload: PaymentStatusUpdate, db: Session = Depends(get_db)
):
    service = PaymentService(db)
    updated = service.update_status(payment_id, payload.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated
