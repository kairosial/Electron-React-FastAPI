"""
Application configuration management using Pydantic settings.

모든 환경변수와 애플리케이션 설정을 중앙에서 관리합니다.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class DatabaseSettings(BaseSettings):
    """데이터베이스 관련 설정"""

    url: str = Field(
        default="sqlite+aiosqlite:///./data/kiosk.db",
        description="Database connection URL"
    )
    echo: bool = Field(
        default=False,
        description="SQLAlchemy echo mode for SQL debugging"
    )
    pool_size: int = Field(
        default=5,
        description="Connection pool size"
    )

    class Config:
        env_prefix = "DB_"


class CORSSettings(BaseSettings):
    """CORS 관련 설정"""

    origins: List[str] = Field(
        default=[
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5173",
        ],
        description="Allowed CORS origins"
    )
    allow_credentials: bool = Field(default=True)
    allow_methods: List[str] = Field(default=["*"])
    allow_headers: List[str] = Field(default=["*"])

    class Config:
        env_prefix = "CORS_"


class StorageSettings(BaseSettings):
    """파일 저장소 관련 설정"""

    upload_dir: str = Field(
        default="./uploads",
        description="Directory for uploaded original images"
    )
    output_dir: str = Field(
        default="./output",
        description="Directory for generated images"
    )
    max_file_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        description="Maximum file size in bytes"
    )
    allowed_extensions: List[str] = Field(
        default=["jpg", "jpeg", "png"],
        description="Allowed file extensions"
    )

    class Config:
        env_prefix = "STORAGE_"


class FaceFusionSettings(BaseSettings):
    """FaceFusion AI 서비스 관련 설정"""

    mode: str = Field(
        default="real",
        description="FaceFusion mode: 'mock' or 'real'"
    )
    project_path: str = Field(
        default="../facefusion",
        description="Path to facefusion project directory (added to sys.path for import)"
    )
    face_swapper_model: str = Field(
        default="inswapper_128",
        description="Face swapper model to use (e.g., 'inswapper_128', 'blendswap_256')"
    )
    execution_providers: List[str] = Field(
        default=["cpu"],
        description="Execution providers for ONNX (e.g., ['cpu'], ['cuda'], ['coreml'])"
    )

    class Config:
        env_prefix = "FACEFUSION_"


class SchedulerSettings(BaseSettings):
    """스케줄러 관련 설정"""

    enabled: bool = Field(
        default=False,
        description="Enable scheduler for data cleanup (set to true in production)"
    )
    cleanup_interval_hours: int = Field(
        default=24,
        description="Interval between cleanup jobs in hours"
    )
    data_retention_days: int = Field(
        default=10,
        description="Number of days to retain participation data"
    )

    class Config:
        env_prefix = "SCHEDULER_"


class Settings(BaseSettings):
    """전체 애플리케이션 설정"""

    # Application info
    app_name: str = Field(
        default="나는솔로 키오스크 백엔드",
        description="Application name"
    )
    app_version: str = Field(
        default="1.0.0",
        description="Application version"
    )
    api_version: str = Field(
        default="v1",
        description="API version prefix"
    )

    # Environment
    environment: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )
    debug: bool = Field(
        default=True,
        description="Debug mode"
    )

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    reload: bool = Field(
        default=True,
        description="Auto-reload on code changes (development only)"
    )

    # Nested settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    facefusion: FaceFusionSettings = Field(default_factory=FaceFusionSettings)
    scheduler: SchedulerSettings = Field(default_factory=SchedulerSettings)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def is_development(self) -> bool:
        """개발 환경 여부"""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """프로덕션 환경 여부"""
        return self.environment == "production"

    @property
    def api_prefix(self) -> str:
        """API 경로 prefix"""
        return f"/api/{self.api_version}"


# 싱글톤 인스턴스
settings = Settings()
