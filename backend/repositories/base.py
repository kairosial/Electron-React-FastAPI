"""
Base Repository

모든 Repository가 상속받는 기본 CRUD 기능을 제공합니다.
"""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import Base

# Generic Type Variable for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    기본 Repository 클래스

    제네릭을 사용하여 모든 모델에 대해 공통 CRUD 작업을 제공합니다.
    """

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        Args:
            model: SQLAlchemy 모델 클래스
            db: 비동기 데이터베이스 세션
        """
        self.model = model
        self.db = db

    async def create(self, **kwargs) -> ModelType:
        """
        새로운 레코드 생성

        Args:
            **kwargs: 모델 필드에 해당하는 키워드 인자

        Returns:
            생성된 모델 인스턴스
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        ID로 레코드 조회

        Args:
            id: Primary key

        Returns:
            모델 인스턴스 또는 None
        """
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        모든 레코드 조회 (페이지네이션)

        Args:
            skip: 건너뛸 레코드 수
            limit: 가져올 최대 레코드 수

        Returns:
            모델 인스턴스 리스트
        """
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, instance: ModelType, **kwargs) -> ModelType:
        """
        레코드 업데이트

        Args:
            instance: 업데이트할 모델 인스턴스
            **kwargs: 업데이트할 필드와 값

        Returns:
            업데이트된 모델 인스턴스
        """
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        """
        레코드 삭제

        Args:
            instance: 삭제할 모델 인스턴스
        """
        await self.db.delete(instance)
        await self.db.flush()

    async def count(self) -> int:
        """
        전체 레코드 수 조회

        Returns:
            레코드 수
        """
        result = await self.db.execute(select(self.model))
        return len(list(result.scalars().all()))
