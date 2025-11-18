"""
참여 세션 스키마

Participation 요청/응답 스키마
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ParticipationCreate(BaseModel):
    """참여 세션 생성 요청 스키마"""

    gender: str = Field(..., description="사용자 성별 (male/female)")
    original_image_path: str = Field(..., description="촬영한 원본 이미지 경로")
    consent_agreed: bool = Field(
        default=False, description="개인정보 수집/이용 동의 여부"
    )


class ParticipationUpdate(BaseModel):
    """참여 세션 업데이트 요청 스키마"""

    consent_agreed: Optional[bool] = Field(None, description="동의 여부")
    selected_profile_id: Optional[int] = Field(None, description="선택된 프로필 ID")
    selected_talent_id: Optional[int] = Field(None, description="선택된 장기자랑 ID")
    generated_profile_image_path: Optional[str] = Field(
        None, description="생성된 프로필 이미지 경로"
    )
    generated_talent_image_path: Optional[str] = Field(
        None, description="생성된 장기자랑 이미지 경로"
    )


class ParticipationResponse(BaseModel):
    """참여 세션 응답 스키마"""

    participation_id: int = Field(..., description="참여 세션 ID")
    consent_agreed: bool = Field(..., description="동의 여부")
    gender: str = Field(..., description="사용자 성별")
    original_image_path: str = Field(..., description="원본 이미지 경로")
    selected_profile_id: Optional[int] = Field(None, description="선택된 프로필 ID")
    selected_talent_id: Optional[int] = Field(None, description="선택된 장기자랑 ID")
    generated_profile_image_path: Optional[str] = Field(
        None, description="생성된 프로필 이미지 경로"
    )
    generated_talent_image_path: Optional[str] = Field(
        None, description="생성된 장기자랑 이미지 경로"
    )
    download_page_uuid: str = Field(..., description="다운로드 페이지 UUID")
    created_at: datetime = Field(..., description="생성 시각")

    model_config = ConfigDict(from_attributes=True)
