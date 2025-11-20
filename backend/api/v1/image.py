"""
Image API Routes

이미지 생성 관련 2개 엔드포인트를 제공합니다.
"""

from fastapi import APIRouter, Depends, status

from backend.services.image_service import ImageService
from backend.core.dependencies import get_image_service
from backend.utils.response import create_success_response

router = APIRouter(prefix="/session")


# 1. POST /session/{participation_id}/generate-profile - 프로필 생성 (화면 #6)
@router.post("/{participation_id}/generate-profile")
async def generate_profile(
    participation_id: int,
    service: ImageService = Depends(get_image_service)
):
    """
    프로필 이미지 생성

    - **participation_id**: 참여 ID
    - 이미 업로드된 원본 이미지와 성별 정보를 사용하여 프로필 이미지 생성
    - 성별에 맞는 프로필 중 랜덤 선택
    """
    result = await service.generate_profile(participation_id)
    return create_success_response(
        data=result,
        message="Profile image generated successfully"
    )


# 2. POST /session/{participation_id}/generate-talent - 장기자랑 생성 (화면 #8)
@router.post("/{participation_id}/generate-talent")
async def generate_talent(
    participation_id: int,
    service: ImageService = Depends(get_image_service)
):
    """
    장기자랑 이미지 생성

    - **participation_id**: 참여 ID
    - 이미 업로드된 원본 이미지와 성별 정보를 사용하여 장기자랑 이미지 생성
    - 성별에 맞는 장기자랑 중 랜덤 선택
    """
    result = await service.generate_talent(participation_id)
    return create_success_response(
        data=result,
        message="Talent image generated successfully"
    )
