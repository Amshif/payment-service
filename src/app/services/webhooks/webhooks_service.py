from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.webhooks_repository import WebhookRepository
from app.repositories.payments_repository import PaymentRepository
from app.services.payments.payments_service import PaymentService
from app.models.payments import PaymentStatus
from .parsers.base import WebhookParserInterface


class WebhookService:
    def __init__(self, db: Session, webhook_repo: WebhookRepository, parser: WebhookParserInterface):
        self.db = db
        self.repo = webhook_repo
        self.parser = parser

        self.handlers = {
            "payment.captured": self._handle_payment_captured,
            "payment.failed": self._handle_payment_failed,
            "refund.processed": self._handle_refund_processed,
            "refund.failed": self._handle_refund_failed,
        }

    def receive(self, event_id: str, event_type: str, payload: dict):
        exists = self.repo.get_by_event_id(event_id)
        if exists:
            return exists

        hook = self.repo.create({
            "event_id": event_id,
            "event_type": event_type,
            "payload": payload,
        })

        self.db.commit()
        self.db.refresh(hook)
        return hook

    def process_event(self, hook):
        try:
            print("Processing webhook ID:", hook.id)
            event_type = hook.event_type
            print("Processing webhook event:", event_type)

            handler = self.handlers.get(event_type)

            if handler:
                handler(hook)   
            else:
                # Unknown event — ignore safely
                pass

            hook.processed = True
            hook.processed_at = datetime.utcnow()
            hook.processing_error = None

        except Exception as e:
            hook.processed = True
            hook.processed_at = datetime.utcnow()
            hook.processing_error = str(e)

        self.db.flush()
        return hook

 

    def _handle_payment_captured(self, hook):
        """
        Razorpay event: payment.captured
        Update payment in local DB to 'captured'
        """
        payment_id = self.parser.get_payment_id(hook.payload)

        service = PaymentService(
            db=self.db,
            payment_repo=PaymentRepository(self.db)
        )
        service.update_status_by_razorpay_id(payment_id, PaymentStatus.captured)

    def _handle_payment_failed(self, hook):
        """
        Razorpay event: payment.failed
        Update payment to 'failed'
        """
        payment_id = self.parser.get_payment_id(hook.payload)

        service = PaymentService(
            db=self.db,
            payment_repo=PaymentRepository(self.db)
        )
        service.update_status_by_razorpay_id(payment_id, PaymentStatus.failed)

    def _handle_refund_processed(self, hook):
        """
        Razorpay event: refund.processed
        TODO: integrate RefundService
        """
        refund_id = self.parser.get_refund_id(hook.payload)
        # TODO: connect with your RefundService
        # refund_service.update_status(refund_id, "processed")
        pass

    def _handle_refund_failed(self, hook):
        """
        Razorpay event: refund.failed
        """
        refund_id = self.parser.get_refund_id(hook.payload)
        # TODO: update refund status in DB
        pass
