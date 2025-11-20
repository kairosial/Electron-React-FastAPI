"""
Target API Routes

프로필/장기자랑 목록 조회 2개 엔드포인트를 제공합니다.
"""

from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.repositories.profile_repo import ProfileRepository
from backend.repositories.talent_repo import TalentRepository
from backend.utils.response import create_success_response

router = APIRouter(prefix="")


# 1. GET /profiles - 프로필 목록 조회
@router.get("/profiles")
async def get_profiles(
    gender: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    프로필 목록 조회

    - **gender**: 성별 필터 (optional: 'male' 또는 'female')
    """
    repo = ProfileRepository(db)

    if gender:
        profiles = await repo.get_by_gender(gender)
    else:
        profiles = await repo.get_all()

    # 모델을 딕셔너리로 변환
    result = [
        {
            "profile_id": p.profile_id,
            "profile_name": p.profile_name,
            "gender_filter": p.gender_filter,
            "target_image_path": p.target_image_path,
        }
        for p in profiles
    ]

    return create_success_response(
        data=result,
        message="Profiles retrieved successfully"
    )


# 2. GET /talents - 장기자랑 목록 조회
@router.get("/talents")
async def get_talents(
    gender: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    장기자랑 목록 조회

    - **gender**: 성별 필터 (optional: 'male' 또는 'female')
    """
    repo = TalentRepository(db)

    if gender:
        talents = await repo.get_by_gender(gender)
    else:
        talents = await repo.get_all()

    # 모델을 딕셔너리로 변환
    result = [
        {
            "talent_id": t.talent_id,
            "talent_name": t.talent_name,
            "gender_filter": t.gender_filter,
            "target_image_path": t.target_image_path,
        }
        for t in talents
    ]

    return create_success_response(
        data=result,
        message="Talents retrieved successfully"
    )
