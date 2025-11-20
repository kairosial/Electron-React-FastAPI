"""
Statistics Service

통계 및 대시보드 비즈니스 로직을 처리합니다.
"""

from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.participation_history_repo import ParticipationHistoryRepository


class StatisticsService:
    """통계 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.history_repo = ParticipationHistoryRepository(db)

    async def get_statistics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """
        전체 통계 조회 (관리자 대시보드)

        Args:
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)

        Returns:
            통계 데이터
        """
        # 날짜 파싱
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        # 통계 조회
        stats = await self.history_repo.get_statistics(start_dt, end_dt)

        return {
            "total_participations": stats.get("total_participations", 0),
            "gender_distribution": stats.get("gender_distribution", {}),
            "popular_profiles": stats.get("popular_profiles", []),
            "popular_talents": stats.get("popular_talents", []),
            "qr_scan_rate": stats.get("qr_scan_rate", 0.0),
            "download_rate_profile": stats.get("download_rate_profile", 0.0),
            "download_rate_talent": stats.get("download_rate_talent", 0.0),
            "print_rate_profile": stats.get("print_rate_profile", 0.0),
            "print_rate_talent": stats.get("print_rate_talent", 0.0),
        }

    async def get_daily_stats(self, days: int = 7) -> list:
        """
        일별 통계 조회 (관리자 대시보드)

        Args:
            days: 조회할 일수 (1-90)

        Returns:
            일별 통계 리스트

        Raises:
            ValueError: days 범위 초과
        """
        # 검증
        if days < 1 or days > 90:
            raise ValueError("days must be between 1 and 90")

        # 일별 통계 조회
        daily_stats = await self.history_repo.get_daily_statistics(days)

        return daily_stats
