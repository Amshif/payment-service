from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payments.refunds_service import RefundService
from app.schemas.refunds import RefundResponse
from app.services.payments.refunds_service import RefundService
from app.repositories.refunds_repository import RefundRepository

router = APIRouter(prefix="/refunds", tags=["Refunds"])


@router.get("/{refund_id}", response_model=RefundResponse)
def get_refund(refund_id: str, db: Session = Depends(get_db)):
    service = RefundService(db, RefundRepository(db))
    return service.get_refund(refund_id)


@router.get("/payment/{payment_id}", response_model=list[RefundResponse])
def list_refunds(payment_id: str, db: Session = Depends(get_db)):
    service = RefundService(db, RefundRepository(db))
    return service.list_refunds(payment_id)
