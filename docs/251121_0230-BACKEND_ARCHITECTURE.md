# FastAPI 백엔드 아키텍처 설계

> API 명세서 기반 구조적 백엔드 서버 설계

**작성일**: 2025-11-21
**버전**: 1.0.0

---

## 📋 목차

- [개요](#개요)
- [아키텍처 원칙](#아키텍처-원칙)
- [디렉토리 구조](#디렉토리-구조)
- [레이어 구조](#레이어-구조)
- [구현 가이드](#구현-가이드)
- [API 엔드포인트 매핑](#api-엔드포인트-매핑)

---

## 개요

### 현재 문제점

- **main.py 비대화**: 479줄, 14개 엔드포인트가 한 파일에 집중
- **비즈니스 로직 혼재**: 라우트 핸들러에 로직 직접 구현
- **테스트 불가능**: 서비스 레이어 미분리로 단위 테스트 어려움
- **확장성 부족**: 새 기능 추가 시 main.py 수정 필수

### 해결 방안

- **Clean Architecture** 적용 (Layered Architecture)
- **모듈화된 라우터**: 도메인별 파일 분리
- **서비스 레이어 도입**: 비즈니스 로직 분리
- **의존성 주입**: 테스트 가능한 구조

---

## 아키텍처 원칙

### 1. 관심사 분리 (Separation of Concerns)

```
Presentation Layer (API Routes)
         ↓
Business Logic Layer (Services)
         ↓
Data Access Layer (Repositories)
         ↓
Database Layer (Models)
```

### 2. 의존성 역전 원칙 (Dependency Inversion)

- 상위 레이어는 하위 레이어의 인터페이스에만 의존
- 구현 세부사항은 주입을 통해 제공

### 3. 단일 책임 원칙 (Single Responsibility)

- 각 모듈은 하나의 명확한 역할만 수행
- 라우터: HTTP 요청/응답 처리
- 서비스: 비즈니스 로직
- 리포지토리: 데이터 접근

---

## 디렉토리 구조

```
backend/
│
├── api/                          # API 엔드포인트 레이어
│   ├── __init__.py
│   └── v1/                       # API 버전 1
│       ├── __init__.py           # 라우터 집계
│       ├── session.py            # 세션 관리 (5개 엔드포인트)
│       ├── image.py              # 이미지 생성 (2개)
│       ├── target.py             # 타겟 조회 (2개)
│       ├── tracking.py           # 추적 (2개)
│       ├── print.py              # 인쇄 (1개)
│       └── dashboard.py          # 대시보드 (3개)
│
├── core/                         # 핵심 설정 및 의존성
│   ├── __init__.py
│   ├── config.py                 # ✅ 완료: 환경변수 및 설정
│   ├── dependencies.py           # 의존성 주입 컨테이너
│   └── database.py               # DB 세션 관리
│
├── services/                     # 비즈니스 로직 레이어
│   ├── __init__.py
│   ├── session_service.py        # 세션 관리 로직
│   ├── image_service.py          # 이미지 생성 로직
│   ├── tracking_service.py       # 추적 로직
│   ├── print_service.py          # 인쇄 로직
│   └── statistics_service.py     # 통계 로직
│
├── middleware/                   # HTTP 미들웨어
│   ├── __init__.py
│   ├── error_handler.py          # 전역 에러 핸들러
│   └── logging.py                # 요청/응답 로깅
│
├── exceptions/                   # 커스텀 예외
│   ├── __init__.py
│   ├── base.py                   # ✅ 완료: 기본 예외 클래스
│   └── api_exceptions.py         # ✅ 완료: API 예외들
│
├── utils/                        # 유틸리티
│   ├── __init__.py
│   ├── response.py               # ✅ 완료: 응답 포맷팅
│   └── file_handler.py           # ✅ 완료: 파일 처리
│
├── models/                       # ✅ 기존: SQLAlchemy 모델 (5개)
├── repositories/                 # ✅ 기존: 데이터 액세스 (6개)
├── schemas/                      # ✅ 기존: Pydantic 스키마 (6개)
│
├── tests/                        # 테스트
│   ├── __init__.py
│   ├── conftest.py               # Pytest 설정
│   ├── unit/                     # 단위 테스트
│   └── integration/              # 통합 테스트
│
├── main.py                       # FastAPI 앱 초기화
├── database.py                   # ✅ 기존
├── scheduler.py                  # ✅ 기존
└── facefusion_service.py         # ✅ 기존
```

---

## 레이어 구조

### Layer 1: API Routes (Presentation)

**역할**: HTTP 요청을 받아 응답 반환

**책임**:
- 요청 데이터 검증 (Pydantic)
- 서비스 레이어 호출
- HTTP 응답 포맷팅

**예시**: `api/v1/session.py`

```python
from fastapi import APIRouter, Depends, status
from backend.services import SessionService
from backend.schemas import SessionCreateRequest, SessionResponse
from backend.utils import create_success_response

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/start", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(
    request: SessionCreateRequest,
    service: SessionService = Depends(get_session_service)
):
    """세션 시작 (화면 #2)"""
    session = await service.create_session(request.consent_agreed)
    return create_success_response(
        data=session,
        message="Session started successfully"
    )
```

### Layer 2: Services (Business Logic)

**역할**: 비즈니스 로직 처리

**책임**:
- 도메인 로직 구현
- 여러 리포지토리 조율
- 트랜잭션 관리
- 예외 처리

**예시**: `services/session_service.py`

```python
from backend.repositories import ParticipationRepository, ParticipationHistoryRepository
from backend.exceptions import SessionNotFoundException

class SessionService:
    def __init__(self, db: AsyncSession):
        self.participation_repo = ParticipationRepository(db)
        self.history_repo = ParticipationHistoryRepository(db)

    async def create_session(self, consent_agreed: bool) -> dict:
        """새 세션 생성"""
        if not consent_agreed:
            raise InvalidGenderException("consent_agreed", ["true"])

        # Participation 생성
        participation = await self.participation_repo.create({
            "consent_agreed": consent_agreed
        })

        # ParticipationHistory 생성
        await self.history_repo.create_from_participation(participation.participation_id)

        return {
            "participation_id": participation.participation_id,
            "download_page_uuid": participation.download_page_uuid
        }

    async def update_gender(self, participation_id: int, gender: str) -> dict:
        """성별 업데이트 (화면 #3)"""
        # 검증
        if gender not in ["male", "female"]:
            raise InvalidGenderException(gender)

        # 세션 조회
        participation = await self.participation_repo.get_by_id(participation_id)
        if not participation:
            raise SessionNotFoundException(participation_id)

        # 업데이트
        updated = await self.participation_repo.update(
            participation_id,
            {"gender": gender}
        )

        # History 동기화
        await self.history_repo.update_gender(participation_id, gender)

        return {
            "participation_id": updated.participation_id,
            "gender": updated.gender
        }
```

### Layer 3: Repositories (Data Access)

**✅ 기존 코드 활용**

- 이미 구현된 Repository 패턴 유지
- 필요시 메서드만 추가

### Layer 4: Models (Database)

**✅ 기존 코드 활용**

- SQLAlchemy 모델 그대로 사용

---

## 구현 가이드

### 1. core/dependencies.py

```python
"""의존성 주입 컨테이너"""

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.services import (
    SessionService,
    ImageService,
    TrackingService,
    PrintService,
    StatisticsService,
)

# Service 의존성 함수들

async def get_session_service(
    db: AsyncSession = Depends(get_db)
) -> SessionService:
    """SessionService 인스턴스 반환"""
    return SessionService(db)

async def get_image_service(
    db: AsyncSession = Depends(get_db)
) -> ImageService:
    """ImageService 인스턴스 반환"""
    return ImageService(db)

async def get_tracking_service(
    db: AsyncSession = Depends(get_db)
) -> TrackingService:
    """TrackingService 인스턴스 반환"""
    return TrackingService(db)

async def get_print_service(
    db: AsyncSession = Depends(get_db)
) -> PrintService:
    """PrintService 인스턴스 반환"""
    return PrintService(db)

async def get_statistics_service(
    db: AsyncSession = Depends(get_db)
) -> StatisticsService:
    """StatisticsService 인스턴스 반환"""
    return StatisticsService(db)
```

### 2. middleware/error_handler.py

```python
"""전역 에러 핸들러"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from backend.exceptions import AppException

async def app_exception_handler(request: Request, exc: AppException):
    """애플리케이션 예외 핸들러"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

async def validation_exception_handler(request: Request, exc: Exception):
    """Pydantic 검증 에러 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "details": exc.errors() if hasattr(exc, 'errors') else str(exc)
        }
    )
```

### 3. api/v1/__init__.py

```python
"""API v1 라우터 집계"""

from fastapi import APIRouter
from backend.api.v1 import session, image, target, tracking, print_router, dashboard

api_router = APIRouter()

# 각 도메인 라우터 등록
api_router.include_router(session.router)
api_router.include_router(image.router)
api_router.include_router(target.router)
api_router.include_router(tracking.router)
api_router.include_router(print_router.router)
api_router.include_router(dashboard.router)
```

### 4. main.py (리팩토링)

```python
"""FastAPI 애플리케이션 진입점"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.core.config import settings
from backend.middleware.error_handler import app_exception_handler
from backend.exceptions import AppException
from backend.api.v1 import api_router

# FastAPI 앱 생성
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

# 예외 핸들러 등록
app.add_exception_handler(AppException, app_exception_handler)

# 정적 파일 서빙
app.mount("/images", StaticFiles(directory=settings.storage.output_dir), name="images")

# API 라우터 등록
app.include_router(api_router, prefix=settings.api_prefix)

# 헬스 체크
@app.get("/")
async def root():
    return {
        "message": settings.app_name,
        "status": "running",
        "mode": settings.facefusion.mode
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 스케줄러 시작
@app.on_event("startup")
async def startup_event():
    from backend.scheduler import start_scheduler
    await start_scheduler()
```

---

## API 엔드포인트 매핑

### API 명세서 → 라우터 파일 매핑

| 엔드포인트 | 파일 | 서비스 메서드 |
|-----------|------|--------------|
| `POST /api/v1/session/start` | `api/v1/session.py` | `SessionService.create_session()` |
| `PATCH /api/v1/session/{id}/gender` | `api/v1/session.py` | `SessionService.update_gender()` |
| `POST /api/v1/session/{id}/upload-image` | `api/v1/session.py` | `SessionService.upload_image()` |
| `POST /api/v1/session/{id}/generate-profile` | `api/v1/image.py` | `ImageService.generate_profile()` |
| `GET /api/v1/session/{id}/result` | `api/v1/session.py` | `SessionService.get_result()` |
| `POST /api/v1/session/{id}/generate-talent` | `api/v1/image.py` | `ImageService.generate_talent()` |
| `GET /api/v1/session/{uuid}` | `api/v1/session.py` | `SessionService.get_by_uuid()` |
| `GET /api/v1/profiles` | `api/v1/target.py` | (Repository 직접 호출) |
| `GET /api/v1/talents` | `api/v1/target.py` | (Repository 직접 호출) |
| `POST /api/v1/tracking/qr-scan` | `api/v1/tracking.py` | `TrackingService.track_qr_scan()` |
| `POST /api/v1/tracking/download` | `api/v1/tracking.py` | `TrackingService.track_download()` |
| `POST /api/v1/print` | `api/v1/print.py` | `PrintService.create_print_job()` |
| `GET /api/v1/dashboard/statistics` | `api/v1/dashboard.py` | `StatisticsService.get_statistics()` |
| `GET /api/v1/dashboard/daily-stats` | `api/v1/dashboard.py` | `StatisticsService.get_daily_stats()` |

---

## 다음 단계

### 우선순위 1: 핵심 인프라

- [x] `core/config.py` - 설정 관리
- [x] `exceptions/` - 예외 클래스
- [x] `utils/` - 유틸리티
- [ ] `core/dependencies.py` - 의존성 주입
- [ ] `middleware/error_handler.py` - 에러 핸들러

### 우선순위 2: 서비스 레이어

- [ ] `services/session_service.py`
- [ ] `services/image_service.py`
- [ ] `services/tracking_service.py`
- [ ] `services/print_service.py`
- [ ] `services/statistics_service.py`

### 우선순위 3: API 라우터

- [ ] `api/v1/session.py` (5개 엔드포인트)
- [ ] `api/v1/image.py` (2개)
- [ ] `api/v1/target.py` (2개)
- [ ] `api/v1/tracking.py` (2개)
- [ ] `api/v1/print.py` (1개)
- [ ] `api/v1/dashboard.py` (3개)

### 우선순위 4: 통합 및 테스트

- [ ] `main.py` 리팩토링
- [ ] 통합 테스트 작성
- [ ] 기존 엔드포인트 마이그레이션
- [ ] API 문서 업데이트

---

## 예상 효과

| 항목 | 현재 | 개선 후 |
|-----|------|--------|
| main.py 라인 수 | 479줄 | < 100줄 |
| 라우터 파일 수 | 1개 | 6개 (도메인별) |
| 서비스 레이어 | 없음 | 5개 클래스 |
| 테스트 가능성 | 어려움 | 쉬움 (DI) |
| 코드 재사용성 | 낮음 | 높음 |
| 유지보수성 | 낮음 | 높음 |

---

**작성자**: Claude Code
**문서 버전**: 1.0.0
**최종 수정**: 2025-11-21
