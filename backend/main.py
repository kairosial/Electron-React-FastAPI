"""
나는솔로 키오스크 백엔드 서버

리팩토링된 Clean Architecture 기반 FastAPI 애플리케이션
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from backend.core.config import settings
from backend.middleware.error_handler import (
    app_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler,
)
from backend.exceptions import AppException
from backend.api.v1 import api_router
from backend.scheduler import run_cleanup_on_startup, run_daily_cleanup

# 로깅 설정
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="Clean Architecture 기반 나는솔로 키오스크 백엔드 API"
)

# CORS 미들웨어 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

# 예외 핸들러 등록
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 정적 파일 서빙 (생성된 이미지)
app.mount("/images", StaticFiles(directory=settings.storage.output_dir), name="images")

# API 라우터 등록
app.include_router(api_router, prefix=settings.api_prefix)


# 기본 엔드포인트
@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "message": settings.app_name,
        "status": "running",
        "version": settings.app_version,
        "mode": settings.facefusion.mode,
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


# 시작/종료 이벤트
@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API Prefix: {settings.api_prefix}")
    logger.info(f"FaceFusion Mode: {settings.facefusion.mode}")
    logger.info(f"Scheduler Enabled: {settings.scheduler.enabled}")

    # 스케줄러가 활성화된 경우에만 실행
    if settings.scheduler.enabled:
        # 초기 데이터 정리
        await run_cleanup_on_startup()

        # 일일 정리 스케줄러를 백그라운드 태스크로 시작
        import asyncio
        asyncio.create_task(run_daily_cleanup())
    else:
        logger.info("⏸️  데이터 정리 스케줄러가 비활성화되어 있습니다.")

    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("Shutting down application...")


# 개발 서버 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload and settings.is_development,
    )
