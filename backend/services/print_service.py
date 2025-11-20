"""
Print Service

인쇄 관련 비즈니스 로직을 처리합니다.
"""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.participation_repo import ParticipationRepository
from backend.repositories.participation_history_repo import ParticipationHistoryRepository
from backend.repositories.print_log_repo import PrintLogRepository
from backend.exceptions import SessionNotFoundException, ImageNotFoundException


class PrintService:
    """인쇄 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.participation_repo = ParticipationRepository(db)
        self.history_repo = ParticipationHistoryRepository(db)
        self.print_log_repo = PrintLogRepository(db)

    async def create_print_job(
        self,
        participation_id: int,
        image_type: str
    ) -> dict:
        """
        인쇄 작업 생성 (화면 #7-1, #9-1)

        Args:
            participation_id: 참여 ID
            image_type: 이미지 타입 ('profile' 또는 'talent')

        Returns:
            인쇄 로그 정보

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
            ImageNotFoundException: 이미지가 생성되지 않음
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

        # 이미지 생성 여부 확인
        if image_type == "profile":
            if not participation.generated_profile_image_path:
                raise ImageNotFoundException(image_type)
        else:  # talent
            if not participation.generated_talent_image_path:
                raise ImageNotFoundException(image_type)

        # PrintLog 생성
        print_log = await self.print_log_repo.create({
            "participation_id": participation_id,
            "image_type": image_type,
            "printed_at": datetime.now(),
        })

        # History 업데이트 (인쇄 상태)
        await self.history_repo.update_print_status(
            participation_id,
            image_type,
            is_printed=True
        )

        # TODO: 실제 프린터 드라이버/서비스 호출
        # await self._send_to_printer(image_path)

        return {
            "print_log_id": print_log.print_log_id,
            "participation_id": print_log.participation_id,
            "image_type": print_log.image_type,
            "printed_at": print_log.printed_at.isoformat(),
        }

    async def _send_to_printer(self, image_path: str) -> None:
        """
        실제 프린터로 이미지 전송 (추후 구현)

        Args:
            image_path: 인쇄할 이미지 경로
        """
        # TODO: 프린터 드라이버/서비스 연동
        pass
