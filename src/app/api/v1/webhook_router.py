from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.webhooks_repository import WebhookRepository
from app.services.webhooks.webhooks_service import WebhookService
from app.schemas.webhooks import WebhookResponse
from app.core.gateway_parser_provider import get_webhook_parser
from app.services.webhooks.task import process_webhook_async    


router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("", response_model=WebhookResponse)
async def receive_webhook(
    request: Request, background: BackgroundTasks, db: Session = Depends(get_db)
):
    body = await request.json()

    event_id = body.get("id") or body.get("event_id")
    event_type = body.get("event") or body.get("event_type")

    if not event_id or not event_type:
        raise HTTPException(400, "Invalid webhook payload")

    parser = get_webhook_parser()

    service = WebhookService(db=db, webhook_repo=WebhookRepository(db), parser=parser)
    hook = service.receive(event_id, event_type, body)

    # Process async
    background.add_task(process_webhook_async, hook.id)

    return hook
