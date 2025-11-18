"""
프로필 타겟 이미지 모델

예: 광수, 영호, 순자, 영숙 등
사용자가 선택할 수 있는 프로필 목록
"""

from sqlalchemy import Column, Integer, String

from backend.database import Base


class TargetProfile(Base):
    """
    프로필 타겟 이미지 테이블

    사용자가 자신의 사진을 합성할 타겟 프로필을 저장합니다.
    """

    __tablename__ = "target_profile"

    profile_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_name = Column(
        String(100), unique=True, nullable=False, comment="프로필 이름 (예: 광수)"
    )
    gender_filter = Column(
        String(10), nullable=False, comment="매칭될 성별 (male/female)"
    )
    target_image_path = Column(
        String(512), nullable=False, comment="딥페이크 합성에 사용될 타겟 이미지 경로"
    )

    def __repr__(self) -> str:
        return f"<TargetProfile(id={self.profile_id}, name='{self.profile_name}', gender='{self.gender_filter}')>"
