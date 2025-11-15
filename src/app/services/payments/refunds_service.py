import uuid
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.refunds_repository import RefundRepository
from app.repositories.payments_repository import PaymentRepository

from app.models.payments import PaymentStatus
from app.models.refunds import RefundStatus

from app.services.interfaces.payment_gateway import PaymentGateway


class RefundService:
    """
    Handles all refund operations:
    - Create refund (gateway required)
    - Get refund (no gateway)
    - List refunds (no gateway)
    """

    def __init__(
        self,
        db: Session,
        refund_repo: RefundRepository,
        payment_repo: PaymentRepository | None = None,
        gateway: PaymentGateway | None = None,
    ):
        self.db = db
        self.payment_repo = payment_repo
        self.refund_repo = refund_repo
        self.gateway = gateway

    def create_refund(
        self, payment_id: str, amount: int | None = None, reason: str | None = None
    ):
        if not self.gateway:
            raise RuntimeError("RefundService requires a gateway for create_refund().")

        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(404, "Payment not found")

        if payment.status != PaymentStatus.captured:
            raise HTTPException(400, "Only captured payments can be refunded")

        # Call payment gateway
        try:
            gateway_refund = self.gateway.create_refund(
                payment_gateway_id=payment.razorpay_payment_id,
                amount=amount or payment.amount,
                reason=reason,
            )
        except Exception as e:
            raise HTTPException(502, f"Refund gateway error: {str(e)}")

        # DB operations atomic
        try:
            refund_data = {
                "id": uuid.uuid4(),
                "payment_id": payment.id,
                "razorpay_refund_id": gateway_refund["id"],
                "amount": gateway_refund["amount"],
                "currency": gateway_refund["currency"],
                "status": RefundStatus.created,
                "reason": reason,
            }

            refund = self.refund_repo.create(refund_data)

            # Update payment status
            self.payment_repo.update_status(payment_id, PaymentStatus.refunded)

            self.db.commit()
            self.db.refresh(refund)
            return refund

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(500, f"Database error during refund creation: {str(e)}")

        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                500, f"Unexpected error during refund creation: {str(e)}"
            )

    def get_refund(self, refund_id: str):
        refund = self.refund_repo.get_by_id(refund_id)
        if not refund:
            raise HTTPException(404, "Refund not found")
        return refund

    def list_refunds(self, payment_id: str):
        return self.refund_repo.list_by_payment(payment_id)
