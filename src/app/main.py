from fastapi import FastAPI
from app.exceptions.http_exceptions import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.api.v1.payments_router import router as payments_router
from app.api.v1.refunds_router import router as refunds_router
from app.api.v1.webhook_router import router as webhook_router



app = FastAPI()

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(payments_router)
app.include_router(refunds_router)
app.include_router(webhook_router)
