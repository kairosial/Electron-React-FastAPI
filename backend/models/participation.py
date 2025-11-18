"""
참여 세션 모델

각 사용자의 키오스크 체험 세션을 저장합니다.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Participation(Base):
    """
    참여 세션 테이블

    사용자가 키오스크를 사용할 때마다 생성되는 세션 정보를 저장합니다.
    """

    __tablename__ = "participation"

    participation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 동의 및 기본 정보
    consent_agreed = Column(
        Boolean, default=False, nullable=False, comment="개인정보 수집/이용 동의 여부"
    )
    gender = Column(String(10), nullable=False, comment="사용자가 선택한 성별 (male/female)")

    # 원본 이미지
    original_image_path = Column(
        String(512), nullable=False, comment="키오스크에서 촬영한 원본 사진 경로"
    )

    # 선택된 타겟 (Foreign Keys)
    selected_profile_id = Column(
        Integer,
        ForeignKey("target_profile.profile_id", ondelete="SET NULL"),
        nullable=True,
        comment="배정된 프로필 ID (예: 광수)",
    )
    selected_talent_id = Column(
        Integer,
        ForeignKey("target_talent.talent_id", ondelete="SET NULL"),
        nullable=True,
        comment="배정된 장기자랑 ID (예: 기타 연주)",
    )

    # 생성된 결과물
    generated_profile_image_path = Column(
        String(512), nullable=True, comment="최종 생성된 프로필 합성 이미지 경로"
    )
    generated_talent_image_path = Column(
        String(512), nullable=True, comment="최종 생성된 장기자랑 합성 이미지 경로"
    )

    # 다운로드 페이지 UUID
    download_page_uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        comment="QR코드 다운로드 페이지 고유 ID",
    )

    # 타임스탬프
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, comment="세션 생성 시각"
    )

    # Relationships
    selected_profile = relationship("TargetProfile", foreign_keys=[selected_profile_id])
    selected_talent = relationship("TargetTalent", foreign_keys=[selected_talent_id])
    print_logs = relationship(
        "PrintLog", back_populates="participation", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Participation(id={self.participation_id}, uuid='{self.download_page_uuid}', gender='{self.gender}')>"
