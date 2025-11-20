"""Custom exceptions for the application."""

from backend.exceptions.base import AppException
from backend.exceptions.api_exceptions import (
    SessionNotFoundException,
    InvalidGenderException,
    ImageNotFoundException,
    ImageGenerationFailedException,
    FileUploadException,
    InvalidFileTypeException,
    FileSizeExceededException,
    ProfileNotFoundException,
    TalentNotFoundException,
)

__all__ = [
    "AppException",
    "SessionNotFoundException",
    "InvalidGenderException",
    "ImageNotFoundException",
    "ImageGenerationFailedException",
    "FileUploadException",
    "InvalidFileTypeException",
    "FileSizeExceededException",
    "ProfileNotFoundException",
    "TalentNotFoundException",
]
