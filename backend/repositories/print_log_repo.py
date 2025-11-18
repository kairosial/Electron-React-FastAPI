"""
인쇄 기록 Repository

PrintLog 모델에 대한 데이터 접근 로직
"""

from typing import Dict, List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.print_log import PrintLog
from backend.repositories.base import BaseRepository


class PrintLogRepository(BaseRepository[PrintLog]):
    """인쇄 로그 Repository"""

    def __init__(self, db: AsyncSession):
        super().__init__(PrintLog, db)

    async def create_print_log(
        self, participation_id: int, image_type: str
    ) -> PrintLog:
        """
        인쇄 기록 생성

        Args:
            participation_id: 참여 세션 ID
            image_type: 'profile' 또는 'talent'

        Returns:
            생성된 PrintLog
        """
        return await self.create(
            participation_id=participation_id, image_type=image_type
        )

    async def get_logs_by_participation(
        self, participation_id: int
    ) -> List[PrintLog]:
        """
        특정 세션의 인쇄 기록 조회

        Args:
            participation_id: 참여 세션 ID

        Returns:
            PrintLog 리스트
        """
        result = await self.db.execute(
            select(PrintLog)
            .where(PrintLog.participation_id == participation_id)
            .order_by(PrintLog.printed_at.desc())
        )
        return list(result.scalars().all())

    async def get_print_statistics(self) -> Dict[str, int]:
        """
        인쇄 통계 조회

        Returns:
            {'profile': 프로필 인쇄 횟수, 'talent': 장기자랑 인쇄 횟수, 'total': 전체 인쇄 횟수}
        """
        # 프로필 인쇄 횟수
        profile_result = await self.db.execute(
            select(func.count(PrintLog.print_log_id)).where(
                PrintLog.image_type == "profile"
            )
        )
        profile_count = profile_result.scalar() or 0

        # 장기자랑 인쇄 횟수
        talent_result = await self.db.execute(
            select(func.count(PrintLog.print_log_id)).where(
                PrintLog.image_type == "talent"
            )
        )
        talent_count = talent_result.scalar() or 0

        return {
            "profile": profile_count,
            "talent": talent_count,
            "total": profile_count + talent_count,
        }

    async def get_recent_prints(self, limit: int = 10) -> List[PrintLog]:
        """
        최근 인쇄 기록 조회

        Args:
            limit: 가져올 최대 개수

        Returns:
            PrintLog 리스트 (최신순)
        """
        result = await self.db.execute(
            select(PrintLog).order_by(PrintLog.printed_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
