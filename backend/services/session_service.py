"""
Session Service

세션 관리 비즈니스 로직을 처리합니다.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from backend.repositories.participation_repo import ParticipationRepository
from backend.repositories.participation_history_repo import ParticipationHistoryRepository
from backend.exceptions import (
    SessionNotFoundException,
    InvalidGenderException,
)
from backend.utils.file_handler import FileHandler


class SessionService:
    """세션 관리 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.participation_repo = ParticipationRepository(db)
        self.history_repo = ParticipationHistoryRepository(db)
        self.file_handler = FileHandler()

    async def create_session(self, consent_agreed: bool) -> dict:
        """
        새 세션 생성 (화면 #2)

        Args:
            consent_agreed: 개인정보 수집 동의 여부

        Returns:
            생성된 세션 정보

        Raises:
            ValueError: consent_agreed가 False인 경우
        """
        if not consent_agreed:
            raise ValueError("Consent must be agreed")

        # Participation 생성
        participation = await self.participation_repo.create({
            "consent_agreed": consent_agreed
        })

        # ParticipationHistory 생성
        await self.history_repo.create_from_participation(
            participation.participation_id
        )

        return {
            "participation_id": participation.participation_id,
            "download_page_uuid": participation.download_page_uuid,
        }

    async def update_gender(self, participation_id: int, gender: str) -> dict:
        """
        성별 업데이트 (화면 #3)

        Args:
            participation_id: 참여 ID
            gender: 성별 ('male' 또는 'female')

        Returns:
            업데이트된 세션 정보

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
            InvalidGenderException: 유효하지 않은 성별
        """
        # 검증
        if gender not in ["male", "female"]:
            raise InvalidGenderException(gender)

        # 세션 조회
        participation = await self.participation_repo.get_by_id(participation_id)
        if not participation:
            raise SessionNotFoundException(participation_id)

        # 업데이트
        updated = await self.participation_repo.update(
            participation_id,
            {"gender": gender}
        )

        # History 동기화
        await self.history_repo.update_gender(participation_id, gender)

        return {
            "participation_id": updated.participation_id,
            "gender": updated.gender,
        }

    async def upload_image(
        self,
        participation_id: int,
        image: UploadFile
    ) -> dict:
        """
        원본 이미지 업로드 (화면 #4)

        Args:
            participation_id: 참여 ID
            image: 업로드된 이미지 파일

        Returns:
            업로드 결과

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
            InvalidFileTypeException: 지원하지 않는 파일 형식
            FileSizeExceededException: 파일 크기 초과
        """
        # 세션 조회
        participation = await self.participation_repo.get_by_id(participation_id)
        if not participation:
            raise SessionNotFoundException(participation_id)

        # 파일 검증
        self.file_handler.validate_file(image)

        # 파일 저장
        file_path = await self.file_handler.save_upload_file(
            image,
            prefix="original"
        )

        # DB 업데이트
        updated = await self.participation_repo.update(
            participation_id,
            {"original_image_path": file_path}
        )

        return {
            "participation_id": updated.participation_id,
            "original_image_path": updated.original_image_path,
        }

    async def get_result(self, participation_id: int) -> dict:
        """
        결과 조회 (화면 #7-1, #9-1)

        Args:
            participation_id: 참여 ID

        Returns:
            생성된 이미지 및 메타데이터

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
        """
        # 세션 조회 (관계 데이터 포함)
        participation = await self.participation_repo.get_by_id(
            participation_id, load_relations=True
        )
        if not participation:
            raise SessionNotFoundException(participation_id)

        # 프로필 결과
        profile_result = None
        if participation.generated_profile_image_path:
            filename = participation.generated_profile_image_path.split("/")[-1]
            profile_result = {
                "selected_profile_name": participation.selected_profile.profile_name if participation.selected_profile else None,
                "generated_profile_image_path": participation.generated_profile_image_path,
                "image_url": self.file_handler.get_image_url(filename),
            }

        # 장기자랑 결과
        talent_result = None
        if participation.generated_talent_image_path:
            filename = participation.generated_talent_image_path.split("/")[-1]
            talent_result = {
                "selected_talent_name": participation.selected_talent.talent_name if participation.selected_talent else None,
                "generated_talent_image_path": participation.generated_talent_image_path,
                "image_url": self.file_handler.get_image_url(filename),
            }

        return {
            "participation_id": participation.participation_id,
            "gender": participation.gender,
            "profile_result": profile_result,
            "talent_result": talent_result,
            "download_page_uuid": participation.download_page_uuid,
        }

    async def get_by_uuid(self, uuid: str) -> dict:
        """
        UUID로 세션 조회 (화면 #7-2, #9-2: 다운로드 페이지)

        Args:
            uuid: 다운로드 페이지 UUID

        Returns:
            세션 정보

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
        """
        # UUID로 조회 (관계 데이터 포함)
        participation = await self.participation_repo.get_by_uuid(
            uuid, load_relations=True
        )
        if not participation:
            raise SessionNotFoundException(uuid)

        return {
            "participation_id": participation.participation_id,
            "gender": participation.gender,
            "generated_profile_image_path": participation.generated_profile_image_path,
            "generated_talent_image_path": participation.generated_talent_image_path,
            "selected_profile_name": participation.selected_profile.profile_name if participation.selected_profile else None,
            "selected_talent_name": participation.selected_talent.talent_name if participation.selected_talent else None,
        }
