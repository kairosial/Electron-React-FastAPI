"""
Dashboard API Routes

대시보드 통계 관련 3개 엔드포인트를 제공합니다.
"""

from typing import Optional
from fastapi import APIRouter, Depends

from backend.services.statistics_service import StatisticsService
from backend.core.dependencies import get_statistics_service
from backend.utils.response import create_success_response

router = APIRouter(prefix="/dashboard")


# 1. GET /dashboard/statistics - 전체 통계 조회
@router.get("/statistics")
async def get_statistics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    service: StatisticsService = Depends(get_statistics_service)
):
    """
    전체 통계 조회 (관리자)

    - **start_date**: 시작 날짜 (optional, YYYY-MM-DD)
    - **end_date**: 종료 날짜 (optional, YYYY-MM-DD)
    """
    result = await service.get_statistics(start_date, end_date)
    return create_success_response(
        data=result,
        message="Statistics retrieved successfully"
    )


# 2. GET /dashboard/daily-stats - 일별 통계 조회
@router.get("/daily-stats")
async def get_daily_stats(
    days: int = 7,
    service: StatisticsService = Depends(get_statistics_service)
):
    """
    일별 통계 조회 (관리자)

    - **days**: 조회할 일수 (default: 7, max: 90)
    """
    result = await service.get_daily_stats(days)
    return create_success_response(
        data=result,
        message="Daily statistics retrieved successfully"
    )
