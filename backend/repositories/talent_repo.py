"""
장기자랑 타겟 Repository

TargetTalent 모델에 대한 데이터 접근 로직
"""

import random
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.target_talent import TargetTalent
from backend.repositories.base import BaseRepository


class TalentRepository(BaseRepository[TargetTalent]):
    """장기자랑 타겟 Repository"""

    def __init__(self, db: AsyncSession):
        super().__init__(TargetTalent, db)

    async def get_by_id(self, talent_id: int) -> Optional[TargetTalent]:
        """
        장기자랑 ID로 조회

        Args:
            talent_id: 장기자랑 ID

        Returns:
            TargetTalent 또는 None
        """
        result = await self.db.execute(
            select(TargetTalent).where(TargetTalent.talent_id == talent_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[TargetTalent]:
        """
        장기자랑 이름으로 조회

        Args:
            name: 장기자랑 이름 (예: '기타 연주')

        Returns:
            TargetTalent 또는 None
        """
        result = await self.db.execute(
            select(TargetTalent).where(TargetTalent.talent_name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_gender(self, gender: str) -> List[TargetTalent]:
        """
        성별로 필터링된 장기자랑 목록 조회

        Args:
            gender: 'male' 또는 'female'

        Returns:
            TargetTalent 리스트
        """
        result = await self.db.execute(
            select(TargetTalent).where(TargetTalent.gender_filter == gender)
        )
        return list(result.scalars().all())

    async def get_random_by_gender(self, gender: str) -> Optional[TargetTalent]:
        """
        성별에 맞는 랜덤 장기자랑 선택

        Args:
            gender: 'male' 또는 'female'

        Returns:
            랜덤으로 선택된 TargetTalent 또는 None
        """
        talents = await self.get_by_gender(gender)
        if not talents:
            return None
        return random.choice(talents)

    async def get_all_talents(self) -> List[TargetTalent]:
        """
        모든 장기자랑 조회

        Returns:
            TargetTalent 리스트
        """
        result = await self.db.execute(select(TargetTalent))
        return list(result.scalars().all())
