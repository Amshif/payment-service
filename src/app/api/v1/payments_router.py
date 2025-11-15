from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payments.payments_service import PaymentService
from app.schemas.payments import PaymentCreate, PaymentResponse, PaymentStatusUpdate
from app.schemas.refunds import RefundCreate, RefundResponse
from app.services.payments.payment_create_service import PaymentCreateService
from app.repositories.payments_repository import PaymentRepository
from app.repositories.refunds_repository import RefundRepository
from app.services.payments.refunds_service import RefundService
from app.core.gateway_provider import get_payment_gateway

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("", response_model=PaymentResponse)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    service = PaymentCreateService(
        db=db,
        payment_repo=PaymentRepository(db),
        gateway=get_payment_gateway(),
    )
    payment = service.create_payment(payload)
    return payment


@router.post("/{payment_id}/refund", response_model=RefundResponse)
def create_refund(
    payment_id: str, payload: RefundCreate, db: Session = Depends(get_db)
):
    service = RefundService(
        db=db,
        payment_repo=PaymentRepository(db),
        refund_repo=RefundRepository(db),
        gateway=get_payment_gateway(),
    )
    refund = service.create_refund(
        payment_id, amount=payload.amount, reason=payload.reason
    )
    return refund


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    service = PaymentService(db=db, payment_repo=PaymentRepository(db))
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.patch("/{payment_id}/status", response_model=PaymentResponse)
def update_payment_status(
    payment_id: str, payload: PaymentStatusUpdate, db: Session = Depends(get_db)
):
    service = PaymentService(db=db, payment_repo=PaymentRepository(db))
    updated = service.update_status(payment_id, payload.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated
