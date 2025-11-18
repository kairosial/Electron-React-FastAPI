"""
타겟(프로필/장기자랑) 스키마

TargetProfile과 TargetTalent 응답 스키마
"""

from pydantic import BaseModel, ConfigDict, Field


class TargetProfileResponse(BaseModel):
    """프로필 타겟 응답 스키마"""

    profile_id: int = Field(..., description="프로필 ID")
    profile_name: str = Field(..., description="프로필 이름 (예: 광수)")
    gender_filter: str = Field(..., description="매칭될 성별 (male/female)")
    target_image_path: str = Field(..., description="타겟 이미지 경로")

    model_config = ConfigDict(from_attributes=True)


class TargetTalentResponse(BaseModel):
    """장기자랑 타겟 응답 스키마"""

    talent_id: int = Field(..., description="장기자랑 ID")
    talent_name: str = Field(..., description="장기자랑 이름 (예: 기타 연주)")
    gender_filter: str = Field(..., description="매칭될 성별 (male/female)")
    target_image_path: str = Field(..., description="타겟 이미지 경로")

    model_config = ConfigDict(from_attributes=True)
