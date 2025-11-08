import uuid
from app.repositories.payments_repository import PaymentRepository
from app.utils.gateway_client import RazorpayClient
from app.models.payments import PaymentStatus

class PaymentService:
    def __init__(self, db):
        self.repo = PaymentRepository(db)
        self.gateway = RazorpayClient()

    def create_payment(self, payload):
        razorpay_order = self.gateway.create_order(payload.amount, payload.currency)

        payment_data = {
            "id": uuid.uuid4(),
            "order_id": payload.order_id,
            "razorpay_payment_id": razorpay_order["id"],
            "amount": payload.amount,
            "currency": payload.currency,
            "status": PaymentStatus.created,
            "payment_gateway": "razorpay",
            "capture": payload.capture
        }
        return self.repo.create(payment_data)

    def get_payment(self, payment_id: str):
        return self.repo.get_by_id(payment_id)

    def update_status(self, payment_id: str, new_status: str):
        return self.repo.update_status(payment_id, PaymentStatus(new_status))
