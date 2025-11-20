"""
데이터 접근 계층 (Repository Pattern)

각 모델에 대한 CRUD 작업을 캡슐화합니다.
"""

from .participation_history_repo import ParticipationHistoryRepository
from .participation_repo import ParticipationRepository
from .print_log_repo import PrintLogRepository
from .profile_repo import ProfileRepository
from .talent_repo import TalentRepository

__all__ = [
    "ParticipationRepository",
    "ProfileRepository",
    "TalentRepository",
    "PrintLogRepository",
    "ParticipationHistoryRepository",
]
