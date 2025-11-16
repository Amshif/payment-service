from sqlalchemy.orm import Session
from app.models.webhook import Webhook


class WebhookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Webhook:
        hook = Webhook(**data)
        self.db.add(hook)
        self.db.flush()
        return hook

    def get_by_event_id(self, event_id: str) -> Webhook | None:
        stmt = self.db.query(Webhook).filter(Webhook.event_id == event_id)
        return stmt.first()

    def get_by_id(self, hook_id: str) -> Webhook | None:
        return self.db.get(Webhook, hook_id)

    def mark_processed(self, hook: Webhook, error: str | None = None):
        hook.processed = True
        hook.processing_error = error
        self.db.flush()
