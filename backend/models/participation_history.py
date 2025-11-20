"""
참여 이력 모델

원본 Participation 데이터가 10일 후 삭제되어도 통계 분석이 가능하도록
개인정보를 제외한 메타데이터와 성과 지표만 영구 보관합니다.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from backend.database import Base


class ParticipationHistory(Base):
    """
    참여 이력 테이블 (통계 및 대시보드용)

    개인정보는 제외하고 분석에 필요한 데이터만 보관합니다.
    원본 Participation이 삭제되어도 이 테이블은 유지됩니다.
    """

    __tablename__ = "participation_history"

    history_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 1. 원본 참조 (단순 매핑용, FK 없음)
    original_participation_id = Column(
        Integer, nullable=False, comment="삭제될 원본 테이블의 ID (단순 매핑용)"
    )

    # 2. 분석용 메타데이터 (개인정보 제외)
    gender = Column(String(10), nullable=False, comment="사용자 성별 (male/female)")
    selected_profile_name = Column(
        String(100), nullable=True, comment="선택한 프로필 이름 (예: 광수)"
    )
    selected_talent_name = Column(
        String(100), nullable=True, comment="선택한 장기자랑 이름 (예: 기타 연주)"
    )

    # 3. 오프라인 성과 (인쇄)
    is_printed_profile = Column(
        Boolean, default=False, nullable=False, comment="프로필 사진 인쇄 여부"
    )
    is_printed_talent = Column(
        Boolean, default=False, nullable=False, comment="장기자랑 사진 인쇄 여부"
    )

    # 4. 온라인 성과 (QR 및 다운로드)
    is_download_page_accessed = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="QR 스캔 후 다운로드 페이지 진입 여부",
    )
    download_count_profile = Column(
        Integer, default=0, nullable=False, comment="프로필 사진 다운로드 버튼 클릭 횟수"
    )
    download_count_talent = Column(
        Integer, default=0, nullable=False, comment="장기자랑 사진 다운로드 버튼 클릭 횟수"
    )

    # 5. 시간 정보
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, comment="체험 완료 시간"
    )

    def __repr__(self) -> str:
        return f"<ParticipationHistory(id={self.history_id}, participation_id={self.original_participation_id}, gender='{self.gender}')>"
