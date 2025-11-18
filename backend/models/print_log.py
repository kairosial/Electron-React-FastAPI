"""
인쇄 기록 모델

사용자가 '인쇄하기' 버튼을 누른 기록을 저장합니다.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class PrintLog(Base):
    """
    인쇄 로그 테이블

    사용자가 프로필 또는 장기자랑 이미지를 인쇄한 기록을 추적합니다.
    """

    __tablename__ = "print_log"

    print_log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 어떤 세션에서 인쇄했는지
    participation_id = Column(
        Integer,
        ForeignKey("participation.participation_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="어떤 체험 세션인지 식별",
    )

    # 인쇄 타입
    image_type = Column(
        String(20),
        nullable=False,
        comment="'profile' 또는 'talent' 인쇄 여부",
    )

    # 인쇄 시각
    printed_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, comment="인쇄한 시각"
    )

    # Relationship
    participation = relationship("Participation", back_populates="print_logs")

    def __repr__(self) -> str:
        return f"<PrintLog(id={self.print_log_id}, participation_id={self.participation_id}, type='{self.image_type}')>"
