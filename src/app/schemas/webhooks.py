from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID


class WebhookResponse(BaseModel):
    id: UUID
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    received_at: datetime
    processed: bool
    processed_at: Optional[datetime] = None
    processing_error: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
