from sqlalchemy.orm import Session
from app.models.refunds import Refund

class RefundRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Refund:
        refund = Refund(**data)
        self.db.add(refund)
        self.db.flush()   # apply pending changes without committing
        return refund

    def get_by_id(self, refund_id: str) -> Refund | None:
        return self.db.query(Refund).filter(Refund.id == refund_id).first()

    def list_by_payment(self, payment_id: str):
        return self.db.query(Refund).filter(Refund.payment_id == payment_id).all()
