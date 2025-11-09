from pydantic import BaseModel
from datetime import datetime, timezone

class ErrorResponse(BaseModel):
    id: str
    code: str
    type: str
    message: str
    details: str | None = None
    status_code: int
    timestamp: datetime

    @classmethod
    def build(cls, code: str, type_: str, message: str, status: int, details: str | None = None):
        from uuid import uuid4
        return cls(
            id=f"req_{uuid4().hex[:12]}",
            code=code,
            type=type_,
            message=message,
            details=details,
            status_code=status,
            timestamp=datetime.now(timezone.utc),
        )
