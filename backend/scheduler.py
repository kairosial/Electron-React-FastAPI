"""
백그라운드 스케줄러

10일이 지난 Participation 데이터를 자동으로 삭제합니다.
"""

import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy import delete, select

from backend.database import AsyncSessionLocal
from backend.models.participation import Participation

logger = logging.getLogger(__name__)


async def cleanup_old_participations():
    """
    10일이 지난 Participation 데이터 삭제

    개인정보 보호를 위해 10일 이상 된 참여 데이터를 삭제합니다.
    ParticipationHistory는 유지되므로 통계 분석은 계속 가능합니다.
    """
    try:
        async with AsyncSessionLocal() as session:
            # 10일 전 날짜 계산
            cutoff_date = datetime.utcnow() - timedelta(days=10)

            # 삭제할 데이터 조회
            result = await session.execute(
                select(Participation).where(Participation.created_at < cutoff_date)
            )
            old_participations = list(result.scalars().all())

            if not old_participations:
                logger.info("삭제할 오래된 참여 데이터가 없습니다.")
                return

            # 삭제 실행
            deleted_count = len(old_participations)
            await session.execute(
                delete(Participation).where(Participation.created_at < cutoff_date)
            )
            await session.commit()

            logger.info(
                f"✅ {deleted_count}개의 10일 이상 된 참여 데이터가 삭제되었습니다. "
                f"(기준일: {cutoff_date.strftime('%Y-%m-%d')})"
            )

    except Exception as e:
        logger.error(f"❌ 참여 데이터 정리 중 오류 발생: {e}")


async def run_daily_cleanup():
    """
    매일 자정에 데이터 정리 실행

    24시간마다 cleanup_old_participations()를 실행합니다.
    """
    while True:
        try:
            logger.info("📅 일일 데이터 정리 작업 시작...")
            await cleanup_old_participations()

            # 24시간 대기
            await asyncio.sleep(86400)  # 24시간 = 86400초

        except Exception as e:
            logger.error(f"❌ 스케줄러 실행 중 오류 발생: {e}")
            # 오류 발생 시 1시간 후 재시도
            await asyncio.sleep(3600)


async def run_cleanup_on_startup():
    """
    서버 시작 시 즉시 한 번 실행

    서버가 오랫동안 꺼져 있었을 경우를 대비하여
    시작 시 바로 정리 작업을 실행합니다.
    """
    logger.info("🚀 서버 시작 시 데이터 정리 작업 실행...")
    await cleanup_old_participations()
