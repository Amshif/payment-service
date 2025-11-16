import uuid
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.payments_repository import PaymentRepository
from app.models.payments import PaymentStatus


class PaymentService:
    def __init__(self, db, payment_repo: PaymentRepository):
        self.db = db
        self.payment_repo = payment_repo


    def get_payment(self, payment_id: str):
        return self.payment_repo.get_by_id(payment_id)

    def update_status(self, payment_id: str, new_status: PaymentStatus):
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if not self._is_valid_transition(payment.status, new_status):
            raise HTTPException(status_code=400, detail="Invalid status transition")

        try:
            self.payment_repo.update_status(payment_id, new_status)
            self.db.commit()
            self.db.refresh(payment)
            return payment

        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail="Failed to update payment status"
            )
        
    def update_status_by_razorpay_id(self, razorpay_id: str, new_status: PaymentStatus):
        payment = self.payment_repo.get_by_razorpay_payment_id(razorpay_id)
        if not payment:
            raise HTTPException(404, f"Payment not found for Razorpay ID {razorpay_id}")

        if not self._is_valid_transition(payment.status, new_status):
            raise HTTPException(400, "Invalid status transition")

        try:
            self.payment_repo.update_status(payment.id, new_status)  # use UUID
            self.db.commit()
            self.db.refresh(payment)
            return payment

        except Exception:
            self.db.rollback()
            raise HTTPException(500, "Failed to update payment status via Razorpay ID")    


    def _is_valid_transition(self, current: PaymentStatus, new: PaymentStatus) -> bool:
        allowed = {
            PaymentStatus.created: [PaymentStatus.authorized, PaymentStatus.failed],
            PaymentStatus.authorized: [PaymentStatus.captured, PaymentStatus.failed],
            PaymentStatus.captured: [PaymentStatus.refunded],
            PaymentStatus.failed: [],
            PaymentStatus.refunded: [],
        }
        return new in allowed.get(current, [])
