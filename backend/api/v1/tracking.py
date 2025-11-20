"""
Tracking API Routes

추적 관련 2개 엔드포인트를 제공합니다.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.services.tracking_service import TrackingService
from backend.core.dependencies import get_tracking_service
from backend.utils.response import create_success_response

router = APIRouter(prefix="/tracking")


# Request Models
class QRScanRequest(BaseModel):
    """QR 스캔 추적 요청"""
    participation_id: int


class DownloadRequest(BaseModel):
    """다운로드 추적 요청"""
    participation_id: int
    image_type: str  # 'profile' or 'talent'


# 1. POST /tracking/qr-scan - QR 스캔 추적 (화면 #7-1, #9-1)
@router.post("/qr-scan")
async def track_qr_scan(
    request: QRScanRequest,
    service: TrackingService = Depends(get_tracking_service)
):
    """
    QR 코드 스캔 추적

    - **participation_id**: 참여 ID
    """
    result = await service.track_qr_scan(request.participation_id)
    return create_success_response(
        data=result,
        message="QR scan tracked successfully"
    )


# 2. POST /tracking/download - 다운로드 추적 (화면 #7-2, #9-2)
@router.post("/download")
async def track_download(
    request: DownloadRequest,
    service: TrackingService = Depends(get_tracking_service)
):
    """
    이미지 다운로드 추적

    - **participation_id**: 참여 ID
    - **image_type**: 이미지 타입 ('profile' 또는 'talent')
    """
    result = await service.track_download(
        request.participation_id,
        request.image_type
    )
    return create_success_response(
        data=result,
        message="Download tracked successfully"
    )
