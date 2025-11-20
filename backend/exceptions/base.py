"""
Base exception classes for the application.

모든 커스텀 예외는 이 파일의 기본 클래스를 상속합니다.
"""

from typing import Any, Dict, Optional


class AppException(Exception):
    """
    기본 애플리케이션 예외 클래스

    모든 커스텀 예외는 이 클래스를 상속받습니다.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """예외를 딕셔너리로 변환"""
        return {
            "success": False,
            "message": self.message,
            "details": self.details,
            "status_code": self.status_code,
        }
