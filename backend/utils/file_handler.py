"""
File upload and storage handler.

파일 업로드, 저장, 검증을 처리하는 유틸리티 클래스입니다.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from fastapi import UploadFile

from backend.core.config import settings
from backend.exceptions import (
    InvalidFileTypeException,
    FileSizeExceededException,
    FileUploadException,
)


class FileHandler:
    """파일 업로드 및 저장 핸들러"""

    def __init__(self):
        self.upload_dir = Path(settings.storage.upload_dir)
        self.output_dir = Path(settings.storage.output_dir)
        self.max_file_size = settings.storage.max_file_size
        self.allowed_extensions = settings.storage.allowed_extensions

        # 디렉토리 생성
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file: UploadFile) -> None:
        """
        파일 유효성 검증

        Args:
            file: 업로드된 파일

        Raises:
            InvalidFileTypeException: 지원하지 않는 파일 형식
            FileSizeExceededException: 파일 크기 초과
        """
        # 파일 확장자 검증
        file_ext = self._get_file_extension(file.filename)
        if file_ext not in self.allowed_extensions:
            raise InvalidFileTypeException(
                file_type=file_ext,
                allowed_types=self.allowed_extensions
            )

        # 파일 크기 검증 (실제 크기 확인을 위해 content-length 헤더 사용)
        # Note: UploadFile은 file-like object이므로 실제 크기는 읽어야 알 수 있음
        # 여기서는 간단히 확장자만 검증하고, 실제 저장 시 크기 확인

    async def save_upload_file(
        self,
        file: UploadFile,
        prefix: str = "original"
    ) -> str:
        """
        업로드된 파일을 저장

        Args:
            file: 업로드된 파일
            prefix: 파일명 prefix

        Returns:
            저장된 파일의 경로

        Raises:
            FileUploadException: 파일 저장 실패
        """
        try:
            # 파일명 생성
            file_ext = self._get_file_extension(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            filename = f"{prefix}_{timestamp}_{unique_id}.{file_ext}"

            # 저장 경로
            file_path = self.upload_dir / filename

            # 파일 저장
            content = await file.read()

            # 파일 크기 검증
            if len(content) > self.max_file_size:
                raise FileSizeExceededException(
                    file_size=len(content),
                    max_size=self.max_file_size
                )

            with open(file_path, "wb") as f:
                f.write(content)

            # 상대 경로 반환
            return f"/{settings.storage.upload_dir}/{filename}"

        except (InvalidFileTypeException, FileSizeExceededException):
            raise
        except Exception as e:
            raise FileUploadException(reason=str(e))

    def generate_output_filename(
        self,
        image_type: str,
        participation_id: int
    ) -> str:
        """
        생성된 이미지 파일명 생성

        Args:
            image_type: 이미지 타입 ('profile' 또는 'talent')
            participation_id: 참여 ID

        Returns:
            생성될 파일명
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{image_type}_{timestamp}_{unique_id}.jpg"
        return filename

    def get_output_path(self, filename: str) -> str:
        """
        출력 파일의 전체 경로 반환

        Args:
            filename: 파일명

        Returns:
            전체 파일 경로
        """
        return str(self.output_dir / filename)

    def get_absolute_path(self, relative_path: str) -> str:
        """
        상대 경로를 절대 경로로 변환

        Args:
            relative_path: DB에 저장된 상대 경로 (예: /uploads/file.jpg)

        Returns:
            절대 경로
        """
        # /uploads/file.jpg -> ./uploads/file.jpg -> 절대 경로
        if relative_path.startswith('/'):
            relative_path = relative_path[1:]  # 맨 앞의 / 제거

        return str(Path.cwd() / relative_path)

    def get_image_url(self, filename: str, request_host: str = "http://localhost:8000") -> str:
        """
        이미지 URL 생성

        Args:
            filename: 파일명
            request_host: 요청 호스트

        Returns:
            이미지 접근 URL
        """
        return f"{request_host}/images/{filename}"

    def _get_file_extension(self, filename: Optional[str]) -> str:
        """
        파일 확장자 추출

        Args:
            filename: 파일명

        Returns:
            확장자 (소문자)
        """
        if not filename:
            return ""
        return filename.split(".")[-1].lower()

    def delete_file(self, file_path: str) -> bool:
        """
        파일 삭제

        Args:
            file_path: 파일 경로

        Returns:
            삭제 성공 여부
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
            return False
        except Exception:
            return False
