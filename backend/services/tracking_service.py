"""
Tracking Service

추적 및 분석 비즈니스 로직을 처리합니다.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.participation_repo import ParticipationRepository
from backend.repositories.participation_history_repo import ParticipationHistoryRepository
from backend.exceptions import SessionNotFoundException


class TrackingService:
    """추적 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.participation_repo = ParticipationRepository(db)
        self.history_repo = ParticipationHistoryRepository(db)

    async def track_qr_scan(self, participation_id: int) -> dict:
        """
        QR 코드 스캔 추적 (화면 #7-1, #9-1)

        Args:
            participation_id: 참여 ID

        Returns:
            추적 결과

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
        """
        # 세션 조회
        participation = await self.participation_repo.get_by_id(participation_id)
        if not participation:
            raise SessionNotFoundException(participation_id)

        # History 업데이트
        await self.history_repo.update_qr_scan_status(
            participation_id,
            is_accessed=True
        )

        return {
            "participation_id": participation_id,
            "is_download_page_accessed": True,
        }

    async def track_download(
        self,
        participation_id: int,
        image_type: str
    ) -> dict:
        """
        다운로드 추적 (화면 #7-2, #9-2)

        Args:
            participation_id: 참여 ID
            image_type: 이미지 타입 ('profile' 또는 'talent')

        Returns:
            추적 결과

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
            ValueError: 유효하지 않은 image_type
        """
        # 검증
        if image_type not in ["profile", "talent"]:
            raise ValueError(
                f"Invalid image_type: {image_type}. Must be 'profile' or 'talent'"
            )

        # 세션 조회
        participation = await self.participation_repo.get_by_id(participation_id)
        if not participation:
            raise SessionNotFoundException(participation_id)

        # History 업데이트 (다운로드 카운트 증가)
        download_count = await self.history_repo.increment_download_count(
            participation_id,
            image_type
        )

        return {
            "participation_id": participation_id,
            "image_type": image_type,
            "download_count": download_count,
        }
