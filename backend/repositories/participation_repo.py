"""
참여 세션 Repository

Participation 모델에 대한 데이터 접근 로직
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.participation import Participation
from backend.repositories.base import BaseRepository


class ParticipationRepository(BaseRepository[Participation]):
    """참여 세션 Repository"""

    def __init__(self, db: AsyncSession):
        super().__init__(Participation, db)

    async def get_by_id(
        self, participation_id: int, load_relations: bool = False
    ) -> Optional[Participation]:
        """
        참여 ID로 조회

        Args:
            participation_id: 참여 ID
            load_relations: 관계된 데이터(profile, talent, print_logs)도 함께 로드할지 여부

        Returns:
            Participation 또는 None
        """
        query = select(Participation).where(
            Participation.participation_id == participation_id
        )

        if load_relations:
            query = query.options(
                selectinload(Participation.selected_profile),
                selectinload(Participation.selected_talent),
                selectinload(Participation.print_logs),
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_uuid(
        self, uuid: str, load_relations: bool = False
    ) -> Optional[Participation]:
        """
        다운로드 UUID로 조회

        Args:
            uuid: 다운로드 페이지 UUID
            load_relations: 관계된 데이터도 함께 로드할지 여부

        Returns:
            Participation 또는 None
        """
        query = select(Participation).where(Participation.download_page_uuid == uuid)

        if load_relations:
            query = query.options(
                selectinload(Participation.selected_profile),
                selectinload(Participation.selected_talent),
                selectinload(Participation.print_logs),
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_recent_sessions(
        self, limit: int = 10, load_relations: bool = False
    ) -> List[Participation]:
        """
        최근 세션 목록 조회

        Args:
            limit: 가져올 최대 개수
            load_relations: 관계된 데이터도 함께 로드할지 여부

        Returns:
            Participation 리스트 (최신순)
        """
        query = (
            select(Participation)
            .order_by(Participation.created_at.desc())
            .limit(limit)
        )

        if load_relations:
            query = query.options(
                selectinload(Participation.selected_profile),
                selectinload(Participation.selected_talent),
                selectinload(Participation.print_logs),
            )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_consent(
        self, participation_id: int, consent: bool
    ) -> Optional[Participation]:
        """
        동의 여부 업데이트

        Args:
            participation_id: 참여 ID
            consent: 동의 여부

        Returns:
            업데이트된 Participation 또는 None
        """
        participation = await self.get_by_id(participation_id)
        if not participation:
            return None

        participation.consent_agreed = consent
        await self.db.flush()
        await self.db.refresh(participation)
        return participation

    async def update_profile_image(
        self, participation_id: int, image_path: str
    ) -> Optional[Participation]:
        """
        생성된 프로필 이미지 경로 업데이트

        Args:
            participation_id: 참여 ID
            image_path: 생성된 이미지 경로

        Returns:
            업데이트된 Participation 또는 None
        """
        participation = await self.get_by_id(participation_id)
        if not participation:
            return None

        participation.generated_profile_image_path = image_path
        await self.db.flush()
        await self.db.refresh(participation)
        return participation

    async def update_talent_image(
        self, participation_id: int, image_path: str
    ) -> Optional[Participation]:
        """
        생성된 장기자랑 이미지 경로 업데이트

        Args:
            participation_id: 참여 ID
            image_path: 생성된 이미지 경로

        Returns:
            업데이트된 Participation 또는 None
        """
        participation = await self.get_by_id(participation_id)
        if not participation:
            return None

        participation.generated_talent_image_path = image_path
        await self.db.flush()
        await self.db.refresh(participation)
        return participation

    async def update(
        self, participation_id: int, data: dict
    ) -> Optional[Participation]:
        """
        참여 세션 정보 업데이트 (서비스 레이어용)

        Args:
            participation_id: 참여 ID
            data: 업데이트할 데이터 딕셔너리

        Returns:
            업데이트된 Participation 또는 None
        """
        participation = await self.get_by_id(participation_id)
        if not participation:
            return None

        for key, value in data.items():
            if hasattr(participation, key):
                setattr(participation, key, value)

        await self.db.flush()
        await self.db.refresh(participation)
        return participation
