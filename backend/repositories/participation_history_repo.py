"""
참여 이력 Repository

ParticipationHistory 모델에 대한 데이터 접근 로직
"""

from datetime import datetime, timedelta
from typing import Dict, List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.participation_history import ParticipationHistory
from backend.repositories.base import BaseRepository


class ParticipationHistoryRepository(BaseRepository[ParticipationHistory]):
    """참여 이력 Repository"""

    def __init__(self, db: AsyncSession):
        super().__init__(ParticipationHistory, db)

    async def create_from_participation(
        self, participation_id: int
    ) -> ParticipationHistory:
        """
        Participation 데이터로부터 이력 생성 (초기 생성용)

        Args:
            participation_id: 원본 참여 ID

        Returns:
            생성된 ParticipationHistory
        """
        return await self.create(
            original_participation_id=participation_id,
        )

    async def update_gender(
        self, participation_id: int, gender: str
    ) -> None:
        """
        성별 업데이트

        Args:
            participation_id: 원본 참여 ID
            gender: 성별 ('male' 또는 'female')
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            history.gender = gender
            await self.db.flush()

    async def update_profile(
        self, participation_id: int, profile_name: str
    ) -> None:
        """
        선택된 프로필 정보 업데이트

        Args:
            participation_id: 원본 참여 ID
            profile_name: 선택된 프로필 이름
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            history.selected_profile_name = profile_name
            await self.db.flush()

    async def update_talent(
        self, participation_id: int, talent_name: str
    ) -> None:
        """
        선택된 장기자랑 정보 업데이트

        Args:
            participation_id: 원본 참여 ID
            talent_name: 선택된 장기자랑 이름
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            history.selected_talent_name = talent_name
            await self.db.flush()

    async def update_print_status(
        self, participation_id: int, image_type: str, is_printed: bool
    ) -> None:
        """
        인쇄 상태 업데이트

        Args:
            participation_id: 원본 참여 ID
            image_type: 'profile' 또는 'talent'
            is_printed: 인쇄 여부
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            if image_type == "profile":
                history.is_printed_profile = is_printed
            elif image_type == "talent":
                history.is_printed_talent = is_printed
            await self.db.flush()

    async def update_qr_scan_status(
        self, participation_id: int, is_accessed: bool
    ) -> None:
        """
        QR 스캔 / 다운로드 페이지 접근 상태 업데이트

        Args:
            participation_id: 원본 참여 ID
            is_accessed: 접근 여부
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            history.is_download_page_accessed = is_accessed
            await self.db.flush()

    async def increment_download_count(
        self, participation_id: int, image_type: str
    ) -> int:
        """
        다운로드 횟수 증가

        Args:
            participation_id: 원본 참여 ID
            image_type: 'profile' 또는 'talent'

        Returns:
            업데이트된 다운로드 카운트
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            if image_type == "profile":
                history.download_count_profile += 1
                count = history.download_count_profile
            elif image_type == "talent":
                history.download_count_talent += 1
                count = history.download_count_talent
            else:
                count = 0
            await self.db.flush()
            return count
        return 0

    async def get_statistics(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Dict:
        """
        전체 통계 조회

        Args:
            start_date: 시작 날짜 (선택사항)
            end_date: 종료 날짜 (선택사항)

        Returns:
            통계 데이터
        """
        query = select(ParticipationHistory)

        if start_date:
            query = query.where(ParticipationHistory.created_at >= start_date)
        if end_date:
            query = query.where(ParticipationHistory.created_at <= end_date)

        result = await self.db.execute(query)
        histories = list(result.scalars().all())

        total = len(histories)
        if total == 0:
            return {
                "total_participations": 0,
                "gender_stats": {"male": 0, "female": 0},
                "print_stats": {
                    "profile_printed": 0,
                    "talent_printed": 0,
                    "print_rate": 0.0,
                },
                "download_stats": {
                    "qr_scanned": 0,
                    "qr_scan_rate": 0.0,
                    "total_downloads_profile": 0,
                    "total_downloads_talent": 0,
                },
                "popular_profiles": [],
                "popular_talents": [],
            }

        # 성별 통계
        male_count = sum(1 for h in histories if h.gender == "male")
        female_count = sum(1 for h in histories if h.gender == "female")

        # 인쇄 통계
        profile_printed = sum(1 for h in histories if h.is_printed_profile)
        talent_printed = sum(1 for h in histories if h.is_printed_talent)
        total_prints = profile_printed + talent_printed

        # QR/다운로드 통계
        qr_scanned = sum(1 for h in histories if h.is_download_page_accessed)
        total_downloads_profile = sum(h.download_count_profile for h in histories)
        total_downloads_talent = sum(h.download_count_talent for h in histories)

        # 인기 프로필/장기자랑
        from collections import Counter

        profile_counter = Counter(
            h.selected_profile_name for h in histories if h.selected_profile_name
        )
        talent_counter = Counter(
            h.selected_talent_name for h in histories if h.selected_talent_name
        )

        return {
            "total_participations": total,
            "gender_stats": {"male": male_count, "female": female_count},
            "print_stats": {
                "profile_printed": profile_printed,
                "talent_printed": talent_printed,
                "total_prints": total_prints,
                "print_rate": round((total_prints / (total * 2)) * 100, 2)
                if total > 0
                else 0.0,
            },
            "download_stats": {
                "qr_scanned": qr_scanned,
                "qr_scan_rate": round((qr_scanned / total) * 100, 2)
                if total > 0
                else 0.0,
                "total_downloads_profile": total_downloads_profile,
                "total_downloads_talent": total_downloads_talent,
                "avg_downloads_per_user": round(
                    (total_downloads_profile + total_downloads_talent) / total, 2
                )
                if total > 0
                else 0.0,
            },
            "popular_profiles": [
                {"name": name, "count": count}
                for name, count in profile_counter.most_common(5)
            ],
            "popular_talents": [
                {"name": name, "count": count}
                for name, count in talent_counter.most_common(5)
            ],
        }

    async def get_daily_stats(self, days: int = 7) -> List[Dict]:
        """
        일별 통계 조회 (최근 N일)

        Args:
            days: 조회할 일수

        Returns:
            일별 통계 리스트
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.created_at >= start_date
            )
        )
        histories = list(result.scalars().all())

        # 날짜별로 그룹화
        from collections import defaultdict

        daily_data = defaultdict(lambda: {"count": 0, "prints": 0, "downloads": 0})

        for history in histories:
            date_key = history.created_at.date().isoformat()
            daily_data[date_key]["count"] += 1

            if history.is_printed_profile or history.is_printed_talent:
                daily_data[date_key]["prints"] += 1

            daily_data[date_key]["downloads"] += (
                history.download_count_profile + history.download_count_talent
            )

        # 리스트로 변환 (날짜순 정렬)
        return [
            {"date": date, **stats}
            for date, stats in sorted(daily_data.items(), key=lambda x: x[0])
        ]

    async def get_daily_statistics(self, days: int = 7) -> List[Dict]:
        """
        일별 통계 조회 (get_daily_stats의 별칭)

        Args:
            days: 조회할 일수

        Returns:
            일별 통계 리스트
        """
        return await self.get_daily_stats(days)
