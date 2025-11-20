"""
Print API Routes

인쇄 관련 1개 엔드포인트를 제공합니다.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.services.print_service import PrintService
from backend.core.dependencies import get_print_service
from backend.utils.response import create_success_response

router = APIRouter(prefix="/print")


# Request Model
class PrintRequest(BaseModel):
    """인쇄 요청"""
    participation_id: int
    image_type: str  # 'profile' or 'talent'


# 1. POST /print - 인쇄 작업 생성 (화면 #7-1, #9-1)
@router.post("")
async def create_print_job(
    request: PrintRequest,
    service: PrintService = Depends(get_print_service)
):
    """
    인쇄 작업 생성

    - **participation_id**: 참여 ID
    - **image_type**: 이미지 타입 ('profile' 또는 'talent')
    """
    result = await service.create_print_job(
        request.participation_id,
        request.image_type
    )
    return create_success_response(
        data=result,
        message="Print job started successfully"
    )
