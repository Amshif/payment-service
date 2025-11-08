from app.models.payments import Payment, PaymentStatus
from sqlalchemy.orm import Session

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Payment:
        payment = Payment(**data)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_by_id(self, payment_id: str) -> Payment | None:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_by_razorpay_payment_id(self, razorpay_id: str) -> Payment | None:
        return self.db.query(Payment).filter(Payment.razorpay_payment_id == razorpay_id).first()

    def update_status(self, payment_id: str, status: PaymentStatus) -> Payment | None:
        payment = self.get_by_id(payment_id)
        if not payment:
            return None
        payment.status = status
        self.db.commit()
        self.db.refresh(payment)
        return payment
