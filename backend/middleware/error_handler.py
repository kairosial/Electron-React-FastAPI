"""
Global error handlers for the application.

모든 예외를 일관된 형식으로 응답합니다.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from backend.exceptions import AppException
from backend.core.config import settings


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    애플리케이션 커스텀 예외 핸들러

    Args:
        request: FastAPI 요청 객체
        exc: AppException 또는 하위 예외

    Returns:
        JSON 응답
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Pydantic 검증 에러 핸들러

    Args:
        request: FastAPI 요청 객체
        exc: 검증 에러

    Returns:
        JSON 응답
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "details": exc.errors(),
        }
    )


async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError
) -> JSONResponse:
    """
    데이터베이스 예외 핸들러

    Args:
        request: FastAPI 요청 객체
        exc: SQLAlchemy 에러

    Returns:
        JSON 응답
    """
    # 프로덕션에서는 상세 에러 숨김
    error_detail = str(exc) if settings.is_development else "Database error occurred"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Database error",
            "details": {"error": error_detail} if settings.debug else {}
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    일반 예외 핸들러 (모든 예외의 최종 폴백)

    Args:
        request: FastAPI 요청 객체
        exc: 예외 객체

    Returns:
        JSON 응답
    """
    # 프로덕션에서는 상세 에러 숨김
    error_detail = str(exc) if settings.is_development else "Internal server error"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "details": {"error": error_detail} if settings.debug else {}
        }
    )
