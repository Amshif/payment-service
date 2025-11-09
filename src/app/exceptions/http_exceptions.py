from app.exceptions.models import ErrorResponse
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: HTTPException):
    err = ErrorResponse.build(
        code="HTTP_ERROR",
        type_="HTTPException",
        message=exc.detail,
        status=exc.status_code,
    )
    logger.warning(f"[{err.id}] HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": err.model_dump(mode="json")}  
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    err = ErrorResponse.build(
        code="VALIDATION_FAILED",
        type_="ValidationError",
        message="Invalid request data",
        status=422,
        details=str(exc.errors()),
    )
    logger.warning(f"[{err.id}] ValidationError: {exc.errors()}")
    return JSONResponse(status_code=422, content={"error": err.model_dump(mode="json")})


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    err = ErrorResponse.build(
        code="DB_CONNECTION_FAILED",
        type_="DatabaseError",
        message="Database operation failed",
        status=500,
        details=str(exc.__cause__ or exc),
    )
    logger.error(f"[{err.id}] SQLAlchemyError: {exc}")
    return JSONResponse(status_code=500, content={"error": err.model_dump(mode="json")})


async def generic_exception_handler(request: Request, exc: Exception):
    err = ErrorResponse.build(
        code="INTERNAL_ERROR",
        type_="InternalServerError",
        message="An unexpected error occurred",
        status=500,
        details=str(exc),
    )
    logger.exception(f"[{err.id}] Unhandled Exception: {exc}")
    return JSONResponse(status_code=500, content={"error": err.model_dump(mode="json")})
