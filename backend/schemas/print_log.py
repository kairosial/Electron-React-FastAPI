"""
인쇄 기록 스키마

PrintLog 요청/응답 스키마
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PrintLogCreate(BaseModel):
    """인쇄 기록 생성 요청 스키마"""

    participation_id: int = Field(..., description="참여 세션 ID")
    image_type: str = Field(..., description="인쇄 타입 (profile/talent)")


class PrintLogResponse(BaseModel):
    """인쇄 기록 응답 스키마"""

    print_log_id: int = Field(..., description="인쇄 로그 ID")
    participation_id: int = Field(..., description="참여 세션 ID")
    image_type: str = Field(..., description="인쇄 타입")
    printed_at: datetime = Field(..., description="인쇄 시각")

    model_config = ConfigDict(from_attributes=True)
