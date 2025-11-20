"""
Dependency Injection Container

FastAPI의 의존성 주입 시스템을 활용하여 서비스 인스턴스를 제공합니다.
"""

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db


# 서비스 임포트 (순환 참조 방지를 위해 지연 임포트 사용)
def get_session_service(db: AsyncSession = Depends(get_db)):
    """SessionService 인스턴스 반환"""
    from backend.services.session_service import SessionService
    return SessionService(db)


def get_image_service(db: AsyncSession = Depends(get_db)):
    """ImageService 인스턴스 반환"""
    from backend.services.image_service import ImageService
    return ImageService(db)


def get_tracking_service(db: AsyncSession = Depends(get_db)):
    """TrackingService 인스턴스 반환"""
    from backend.services.tracking_service import TrackingService
    return TrackingService(db)


def get_print_service(db: AsyncSession = Depends(get_db)):
    """PrintService 인스턴스 반환"""
    from backend.services.print_service import PrintService
    return PrintService(db)


def get_statistics_service(db: AsyncSession = Depends(get_db)):
    """StatisticsService 인스턴스 반환"""
    from backend.services.statistics_service import StatisticsService
    return StatisticsService(db)
