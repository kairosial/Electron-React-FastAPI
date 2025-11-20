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
        self,
        participation_id: int,
        gender: str,
        profile_name: str = None,
        talent_name: str = None,
    ) -> ParticipationHistory:
        """
        Participation 데이터로부터 이력 생성

        Args:
            participation_id: 원본 참여 ID
            gender: 성별
            profile_name: 선택한 프로필 이름
            talent_name: 선택한 장기자랑 이름

        Returns:
            생성된 ParticipationHistory
        """
        return await self.create(
            original_participation_id=participation_id,
            gender=gender,
            selected_profile_name=profile_name,
            selected_talent_name=talent_name,
        )

    async def update_print_status(
        self, participation_id: int, image_type: str
    ) -> None:
        """
        인쇄 상태 업데이트

        Args:
            participation_id: 원본 참여 ID
            image_type: 'profile' 또는 'talent'
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            if image_type == "profile":
                history.is_printed_profile = True
            elif image_type == "talent":
                history.is_printed_talent = True
            await self.db.flush()

    async def update_download_page_accessed(self, participation_id: int) -> None:
        """
        다운로드 페이지 접근 상태 업데이트 (QR 스캔)

        Args:
            participation_id: 원본 참여 ID
        """
        result = await self.db.execute(
            select(ParticipationHistory).where(
                ParticipationHistory.original_participation_id == participation_id
            )
        )
        history = result.scalar_one_or_none()

        if history:
            history.is_download_page_accessed = True
            await self.db.flush()

    async def increment_download_count(
        self, participation_id: int, image_type: str
    ) -> None:
        """
        다운로드 횟수 증가

        Args:
            participation_id: 원본 참여 ID
            image_type: 'profile' 또는 'talent'
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
            elif image_type == "talent":
                history.download_count_talent += 1
            await self.db.flush()

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
