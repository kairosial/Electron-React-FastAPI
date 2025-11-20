"""
참여 이력 스키마

ParticipationHistory 요청/응답 스키마
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ParticipationHistoryResponse(BaseModel):
    """참여 이력 응답 스키마"""

    history_id: int = Field(..., description="이력 ID")
    original_participation_id: int = Field(..., description="원본 참여 ID")
    gender: str = Field(..., description="성별")
    selected_profile_name: Optional[str] = Field(None, description="선택한 프로필 이름")
    selected_talent_name: Optional[str] = Field(None, description="선택한 장기자랑 이름")
    is_printed_profile: bool = Field(..., description="프로필 인쇄 여부")
    is_printed_talent: bool = Field(..., description="장기자랑 인쇄 여부")
    is_download_page_accessed: bool = Field(..., description="다운로드 페이지 접근 여부")
    download_count_profile: int = Field(..., description="프로필 다운로드 횟수")
    download_count_talent: int = Field(..., description="장기자랑 다운로드 횟수")
    created_at: datetime = Field(..., description="생성 시각")

    model_config = ConfigDict(from_attributes=True)


class DownloadTrackingRequest(BaseModel):
    """다운로드 추적 요청 스키마"""

    participation_id: int = Field(..., description="참여 세션 ID")
    image_type: str = Field(..., description="이미지 타입 (profile/talent)")


class QRScanTrackingRequest(BaseModel):
    """QR 스캔 추적 요청 스키마"""

    uuid: str = Field(..., description="다운로드 페이지 UUID")
