"""
장기자랑 타겟 이미지 모델

예: 기타 연주, 춤, 노래 등
사용자가 선택할 수 있는 장기자랑 목록
"""

from sqlalchemy import Column, Integer, String

from backend.database import Base


class TargetTalent(Base):
    """
    장기자랑 타겟 이미지 테이블

    사용자가 자신의 사진을 합성할 장기자랑 장면을 저장합니다.
    """

    __tablename__ = "target_talent"

    talent_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    talent_name = Column(
        String(100), unique=True, nullable=False, comment="장기자랑 이름 (예: 기타 연주)"
    )
    gender_filter = Column(
        String(10), nullable=False, comment="매칭될 성별 (male/female)"
    )
    target_image_path = Column(
        String(512), nullable=False, comment="딥페이크 합성에 사용될 타겟 이미지 경로"
    )

    def __repr__(self) -> str:
        return f"<TargetTalent(id={self.talent_id}, name='{self.talent_name}', gender='{self.gender_filter}')>"
