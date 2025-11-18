"""
데이터베이스 연결 및 세션 관리 모듈

SQLite + SQLAlchemy 비동기 방식으로 데이터베이스 연결을 관리합니다.
"""

import os
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 환경 변수에서 DATABASE_URL 가져오기
# 기본값: 프로젝트 루트의 data 폴더에 SQLite DB 생성
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite+aiosqlite:///{DATA_DIR}/kiosk.db"
)

# SQLite 전용 설정
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# 비동기 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL 쿼리 로깅 (개발 환경용, 프로덕션에서는 False 권장)
    future=True,
    connect_args=connect_args,
)

# 비동기 세션 팩토리 생성
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# SQLAlchemy Base 클래스
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency injection용 데이터베이스 세션 제공

    사용 예:
    ```python
    @app.get("/items")
    async def get_items(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Item))
        return result.scalars().all()
    ```

    Yields:
        AsyncSession: 비동기 데이터베이스 세션
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    데이터베이스 초기화

    모든 테이블을 생성합니다.
    실제 프로덕션에서는 Alembic 마이그레이션을 사용해야 합니다.

    Note:
        개발 환경에서만 사용하고, 프로덕션에서는 Alembic을 사용하세요.
    """
    async with engine.begin() as conn:
        # 모든 테이블 생성 (Base를 상속한 모델들)
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """
    데이터베이스의 모든 테이블 삭제

    Warning:
        이 함수는 모든 데이터를 삭제합니다!
        테스트 환경에서만 사용하세요.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
