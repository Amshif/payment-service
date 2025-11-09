import uuid
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.payments_repository import PaymentRepository
from app.repositories.refunds_repository import RefundRepository
from app.utils.gateway_client import RazorpayClient
from app.models.payments import PaymentStatus
from app.models.refunds import RefundStatus


class PaymentService:
    def __init__(self, db):
        self.db = db
        self.repo = PaymentRepository(db)
        self.refunds_repo = RefundRepository(db)
        self.gateway = RazorpayClient()

    def create_payment(self, payload):
        try:
            # Create Razorpay order
            razorpay_order = self.gateway.create_order(payload.amount, payload.currency)

            # Create payment record
            payment_data = {
                "id": uuid.uuid4(),
                "order_id": payload.order_id,
                "razorpay_payment_id": razorpay_order["id"],
                "amount": payload.amount,
                "currency": payload.currency,
                "status": PaymentStatus.created,
                "payment_gateway": "razorpay",
                "capture": payload.capture,
            }

            payment = self.repo.create(payment_data)
            self.db.commit()
            self.db.refresh(payment)
            return payment

        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail="Database error during payment creation"
            )

        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=502, detail=f"Payment gateway error: {str(e)}"
            )

    def get_payment(self, payment_id: str):
        return self.repo.get_by_id(payment_id)

    def update_status(self, payment_id: str, new_status: PaymentStatus):
        payment = self.repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if not self._is_valid_transition(payment.status, new_status):
            raise HTTPException(status_code=400, detail="Invalid status transition")

        try:
            self.repo.update_status(payment_id, new_status)
            self.db.commit()
            self.db.refresh(payment)
            return payment

        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail="Failed to update payment status"
            )

    def create_refund(
        self, payment_id: str, amount: int | None = None, reason: str | None = None
    ):
        """
        Creates a refund in Razorpay and updates the local DB atomically.
        """
        payment = self.repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if payment.status != PaymentStatus.captured:
            raise HTTPException(
                status_code=400, detail="Only captured payments can be refunded"
            )

        # Create refund on Razorpay
        try:
            razorpay_refund = self.gateway.create_refund(
                razorpay_payment_id=payment.razorpay_payment_id,
                amount=amount or payment.amount,
                reason=reason,
            )
        except Exception as e:
            raise HTTPException(
                status_code=502, detail=f"Refund gateway error: {str(e)}"
            )

        # Create refund record and update payment atomically
        try:
            refund_data = {
                "id": uuid.uuid4(),
                "payment_id": payment.id,
                "razorpay_refund_id": razorpay_refund["id"],
                "amount": razorpay_refund["amount"],
                "currency": razorpay_refund["currency"],
                "status": RefundStatus.created,
                "reason": reason,
            }

            # Create refund entry
            refund = self.refunds_repo.create(refund_data)

            # Update payment status to refunded
            self.repo.update_status(payment_id, PaymentStatus.refunded)

            #  Commit both together
            self.db.commit()
            self.db.refresh(refund)
            return refund

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error during refund creation: {str(e)}",
            )

        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail="Unexpected error during refund creation"
            )

    # ====================================
    # ⚙️ STATUS TRANSITION VALIDATION
    # ====================================
    def _is_valid_transition(self, current: PaymentStatus, new: PaymentStatus) -> bool:
        allowed = {
            PaymentStatus.created: [PaymentStatus.authorized, PaymentStatus.failed],
            PaymentStatus.authorized: [PaymentStatus.captured, PaymentStatus.failed],
            PaymentStatus.captured: [PaymentStatus.refunded],
            PaymentStatus.failed: [],
            PaymentStatus.refunded: [],
        }
        return new in allowed.get(current, [])
