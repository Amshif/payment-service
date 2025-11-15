import uuid
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.payments_repository import PaymentRepository
from app.models.payments import PaymentStatus
from app.services.interfaces.payment_gateway import PaymentGateway


class PaymentCreateService:
   

    def __init__(self, db, payment_repo: PaymentRepository, gateway: PaymentGateway):
        self.db = db
        self.payment_repo = payment_repo
        self.gateway = gateway

    def create_payment(self, payload):
        try:
            # Call Razorpay Gateway
            razorpay_order = self.gateway.create_order(payload.amount, payload.currency)

            # Local DB record
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

            payment = self.payment_repo.create(payment_data)
            self.db.commit()
            self.db.refresh(payment)
            return payment

        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(500, "Database error during payment creation")

        except Exception as e:
            self.db.rollback()
            raise HTTPException(502, f"Payment gateway error: {str(e)}")
