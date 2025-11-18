"""
프로필 타겟 Repository

TargetProfile 모델에 대한 데이터 접근 로직
"""

import random
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.target_profile import TargetProfile
from backend.repositories.base import BaseRepository


class ProfileRepository(BaseRepository[TargetProfile]):
    """프로필 타겟 Repository"""

    def __init__(self, db: AsyncSession):
        super().__init__(TargetProfile, db)

    async def get_by_id(self, profile_id: int) -> Optional[TargetProfile]:
        """
        프로필 ID로 조회

        Args:
            profile_id: 프로필 ID

        Returns:
            TargetProfile 또는 None
        """
        result = await self.db.execute(
            select(TargetProfile).where(TargetProfile.profile_id == profile_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[TargetProfile]:
        """
        프로필 이름으로 조회

        Args:
            name: 프로필 이름 (예: '광수')

        Returns:
            TargetProfile 또는 None
        """
        result = await self.db.execute(
            select(TargetProfile).where(TargetProfile.profile_name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_gender(self, gender: str) -> List[TargetProfile]:
        """
        성별로 필터링된 프로필 목록 조회

        Args:
            gender: 'male' 또는 'female'

        Returns:
            TargetProfile 리스트
        """
        result = await self.db.execute(
            select(TargetProfile).where(TargetProfile.gender_filter == gender)
        )
        return list(result.scalars().all())

    async def get_random_by_gender(self, gender: str) -> Optional[TargetProfile]:
        """
        성별에 맞는 랜덤 프로필 선택

        Args:
            gender: 'male' 또는 'female'

        Returns:
            랜덤으로 선택된 TargetProfile 또는 None
        """
        profiles = await self.get_by_gender(gender)
        if not profiles:
            return None
        return random.choice(profiles)

    async def get_all_profiles(self) -> List[TargetProfile]:
        """
        모든 프로필 조회

        Returns:
            TargetProfile 리스트
        """
        result = await self.db.execute(select(TargetProfile))
        return list(result.scalars().all())
