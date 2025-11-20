"""
Standard response formatting utilities.

모든 API 응답을 일관된 형식으로 반환하기 위한 유틸리티입니다.
"""

from typing import Any, Dict, Optional


def create_success_response(
    data: Any,
    message: str = "Success",
    status_code: int = 200
) -> Dict[str, Any]:
    """
    성공 응답 생성

    Args:
        data: 응답 데이터
        message: 응답 메시지
        status_code: HTTP 상태 코드

    Returns:
        표준 형식의 성공 응답 딕셔너리
    """
    return {
        "success": True,
        "data": data,
        "message": message,
    }


def create_error_response(
    message: str,
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 500
) -> Dict[str, Any]:
    """
    에러 응답 생성

    Args:
        message: 에러 메시지
        details: 추가 에러 세부사항
        status_code: HTTP 상태 코드

    Returns:
        표준 형식의 에러 응답 딕셔너리
    """
    return {
        "success": False,
        "message": message,
        "details": details or {},
    }
