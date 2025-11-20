"""
Image Service

이미지 생성 및 FaceFusion 연동 비즈니스 로직을 처리합니다.
"""

import random
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.participation_repo import ParticipationRepository
from backend.repositories.participation_history_repo import ParticipationHistoryRepository
from backend.repositories.profile_repo import ProfileRepository
from backend.repositories.talent_repo import TalentRepository
from backend.exceptions import (
    SessionNotFoundException,
    ImageGenerationFailedException,
    ProfileNotFoundException,
    TalentNotFoundException,
)
from backend.utils.file_handler import FileHandler
from backend.facefusion_service import FaceFusionService


class ImageService:
    """이미지 생성 서비스"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.participation_repo = ParticipationRepository(db)
        self.history_repo = ParticipationHistoryRepository(db)
        self.profile_repo = ProfileRepository(db)
        self.talent_repo = TalentRepository(db)
        self.file_handler = FileHandler()
        self.facefusion = FaceFusionService()

    async def generate_profile(self, participation_id: int) -> dict:
        """
        프로필 이미지 생성 (화면 #6)

        Args:
            participation_id: 참여 ID

        Returns:
            생성된 프로필 이미지 정보

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
            ImageGenerationFailedException: 이미지 생성 실패
            ProfileNotFoundException: 매칭 가능한 프로필이 없음
        """
        # 세션 조회
        participation = await self.participation_repo.get_by_id(participation_id)
        if not participation:
            raise SessionNotFoundException(participation_id)

        # 원본 이미지 및 성별 확인
        if not participation.original_image_path or not participation.gender:
            raise ImageGenerationFailedException(
                "Original image or gender not set"
            )

        # 성별에 맞는 프로필 목록 조회
        profiles = await self.profile_repo.get_by_gender(participation.gender)
        if not profiles:
            raise ProfileNotFoundException(participation.gender)

        # 랜덤 선택
        selected_profile = random.choice(profiles)

        # 파일명 생성
        filename = self.file_handler.generate_output_filename(
            "profile",
            participation_id
        )
        output_path = self.file_handler.get_output_path(filename)

        # FaceFusion 실행
        try:
            await self.facefusion.generate_image(
                source_path=participation.original_image_path,
                target_path=selected_profile.target_image_path,
                output_path=output_path
            )
        except Exception as e:
            raise ImageGenerationFailedException(str(e))

        # DB 업데이트
        generated_path = f"/output/{filename}"
        updated = await self.participation_repo.update(
            participation_id,
            {
                "selected_profile_id": selected_profile.profile_id,
                "generated_profile_image_path": generated_path,
            }
        )

        # History 업데이트
        await self.history_repo.update_profile(
            participation_id,
            selected_profile.profile_name
        )

        return {
            "participation_id": updated.participation_id,
            "selected_profile_id": selected_profile.profile_id,
            "selected_profile_name": selected_profile.profile_name,
            "generated_profile_image_path": generated_path,
            "image_url": self.file_handler.get_image_url(filename),
        }

    async def generate_talent(self, participation_id: int) -> dict:
        """
        장기자랑 이미지 생성 (화면 #8)

        Args:
            participation_id: 참여 ID

        Returns:
            생성된 장기자랑 이미지 정보

        Raises:
            SessionNotFoundException: 세션을 찾을 수 없음
            ImageGenerationFailedException: 이미지 생성 실패
            TalentNotFoundException: 매칭 가능한 장기자랑이 없음
        """
        # 세션 조회
        participation = await self.participation_repo.get_by_id(participation_id)
        if not participation:
            raise SessionNotFoundException(participation_id)

        # 원본 이미지 및 성별 확인
        if not participation.original_image_path or not participation.gender:
            raise ImageGenerationFailedException(
                "Original image or gender not set"
            )

        # 성별에 맞는 장기자랑 목록 조회
        talents = await self.talent_repo.get_by_gender(participation.gender)
        if not talents:
            raise TalentNotFoundException(participation.gender)

        # 랜덤 선택
        selected_talent = random.choice(talents)

        # 파일명 생성
        filename = self.file_handler.generate_output_filename(
            "talent",
            participation_id
        )
        output_path = self.file_handler.get_output_path(filename)

        # FaceFusion 실행
        try:
            await self.facefusion.generate_image(
                source_path=participation.original_image_path,
                target_path=selected_talent.target_image_path,
                output_path=output_path
            )
        except Exception as e:
            raise ImageGenerationFailedException(str(e))

        # DB 업데이트
        generated_path = f"/output/{filename}"
        updated = await self.participation_repo.update(
            participation_id,
            {
                "selected_talent_id": selected_talent.talent_id,
                "generated_talent_image_path": generated_path,
            }
        )

        # History 업데이트
        await self.history_repo.update_talent(
            participation_id,
            selected_talent.talent_name
        )

        return {
            "participation_id": updated.participation_id,
            "selected_talent_id": selected_talent.talent_id,
            "selected_talent_name": selected_talent.talent_name,
            "generated_talent_image_path": generated_path,
            "image_url": self.file_handler.get_image_url(filename),
        }
