"""
API specific exceptions.

각 도메인별 예외 클래스들을 정의합니다.
"""

from typing import Any, Dict, Optional
from backend.exceptions.base import AppException


# Session related exceptions
class SessionNotFoundException(AppException):
    """세션을 찾을 수 없을 때 발생"""

    def __init__(self, session_id: Any, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Session not found: {session_id}",
            status_code=404,
            details=details or {"session_id": session_id}
        )


class InvalidGenderException(AppException):
    """유효하지 않은 성별 값일 때 발생"""

    def __init__(self, gender: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Invalid gender value: '{gender}'. Must be 'male' or 'female'",
            status_code=400,
            details=details or {"gender": gender, "allowed_values": ["male", "female"]}
        )


# Image related exceptions
class ImageNotFoundException(AppException):
    """이미지를 찾을 수 없을 때 발생"""

    def __init__(self, image_type: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{image_type.capitalize()} image not found or not yet generated",
            status_code=404,
            details=details or {"image_type": image_type}
        )


class ImageGenerationFailedException(AppException):
    """이미지 생성 실패 시 발생"""

    def __init__(self, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Image generation failed: {reason}",
            status_code=500,
            details=details or {"reason": reason}
        )


# File upload related exceptions
class FileUploadException(AppException):
    """파일 업로드 실패 시 발생"""

    def __init__(self, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"File upload failed: {reason}",
            status_code=500,
            details=details or {"reason": reason}
        )


class InvalidFileTypeException(AppException):
    """지원하지 않는 파일 형식일 때 발생"""

    def __init__(
        self,
        file_type: str,
        allowed_types: list,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Invalid file type: '{file_type}'. Allowed types: {', '.join(allowed_types)}",
            status_code=415,
            details=details or {
                "file_type": file_type,
                "allowed_types": allowed_types
            }
        )


class FileSizeExceededException(AppException):
    """파일 크기 초과 시 발생"""

    def __init__(
        self,
        file_size: int,
        max_size: int,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"File size ({file_size} bytes) exceeds maximum allowed size ({max_size} bytes)",
            status_code=413,
            details=details or {
                "file_size": file_size,
                "max_size": max_size
            }
        )


# Target related exceptions
class ProfileNotFoundException(AppException):
    """프로필 타겟을 찾을 수 없을 때 발생"""

    def __init__(self, gender: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        message = f"No profile targets found for gender: {gender}" if gender else "No profile targets found"
        super().__init__(
            message=message,
            status_code=503,
            details=details or {"gender": gender}
        )


class TalentNotFoundException(AppException):
    """장기자랑 타겟을 찾을 수 없을 때 발생"""

    def __init__(self, gender: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        message = f"No talent targets found for gender: {gender}" if gender else "No talent targets found"
        super().__init__(
            message=message,
            status_code=503,
            details=details or {"gender": gender}
        )


# Print related exceptions
class PrintJobFailedException(AppException):
    """인쇄 작업 실패 시 발생"""

    def __init__(self, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Print job failed: {reason}",
            status_code=500,
            details=details or {"reason": reason}
        )


# Tracking related exceptions
class TrackingFailedException(AppException):
    """추적 기록 실패 시 발생"""

    def __init__(self, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Tracking failed: {reason}",
            status_code=500,
            details=details or {"reason": reason}
        )
