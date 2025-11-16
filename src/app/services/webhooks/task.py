from app.core.database import SessionLocal
from app.repositories.webhooks_repository import WebhookRepository
from app.services.webhooks.webhooks_service import WebhookService
from app.core.gateway_parser_provider import get_webhook_parser


def process_webhook_async(hook_id: str):
    db = SessionLocal()

    try:
        repo = WebhookRepository(db)
        hook = repo.get_by_id(hook_id)
        if not hook:
            print("Webhook not found in background task:", hook_id)
            return

        service = WebhookService(
            db=db,
            webhook_repo=repo,
            parser=get_webhook_parser()
        )

        service.process_event(hook)
        db.commit()

    except Exception as e:
        print("Error processing webhook in background:", e)

    finally:
        db.close()
