"""
나는솔로 키오스크 백엔드 서버
FaceFusion 모의 실행 API
"""

from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

import logging
import uvicorn
from pathlib import Path

from backend.database import get_db, init_db
from backend.facefusion_service import FaceFusionService
from backend.repositories import (
    ParticipationRepository,
    PrintLogRepository,
    ProfileRepository,
    TalentRepository,
)
from backend.schemas import (
    ParticipationCreate,
    ParticipationResponse,
    PrintLogCreate,
    PrintLogResponse,
    TargetProfileResponse,
    TargetTalentResponse,
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 초기화
app = FastAPI(
    title="나는솔로 키오스크 API",
    description="FaceFusion 모의 실행을 통한 프로필 및 탤런트 이미지 생성",
    version="1.0.0"
)

# CORS 설정 (프론트엔드에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Alternative port
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 출력 디렉토리 생성
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 정적 파일 서빙 (생성된 이미지 다운로드용)
app.mount("/images", StaticFiles(directory=str(OUTPUT_DIR)), name="images")

# FaceFusion 서비스 초기화
facefusion_service = FaceFusionService(output_dir=OUTPUT_DIR)


# 애플리케이션 시작/종료 이벤트
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 데이터베이스 초기화"""
    logger.info("데이터베이스 초기화 중...")
    await init_db()
    logger.info("✅ 데이터베이스 초기화 완료")


@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 정리 작업"""
    logger.info("서버 종료 중...")


@app.get("/")
async def root():
    """서버 상태 확인 엔드포인트"""
    return {
        "message": "나는솔로 키오스크 백엔드 서버",
        "status": "running",
        "mode": "mock_facefusion"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


# ==================== 새로운 데이터베이스 통합 API ====================


@app.get("/api/profiles", response_model=List[TargetProfileResponse])
async def get_profiles(
    gender: str = None, db: AsyncSession = Depends(get_db)
):
    """
    사용 가능한 프로필 목록 조회

    Args:
        gender: 'male' 또는 'female'로 필터링 (선택사항)
        db: 데이터베이스 세션

    Returns:
        프로필 목록
    """
    repo = ProfileRepository(db)
    if gender:
        profiles = await repo.get_by_gender(gender)
    else:
        profiles = await repo.get_all_profiles()
    return profiles


@app.get("/api/talents", response_model=List[TargetTalentResponse])
async def get_talents(
    gender: str = None, db: AsyncSession = Depends(get_db)
):
    """
    사용 가능한 장기자랑 목록 조회

    Args:
        gender: 'male' 또는 'female'로 필터링 (선택사항)
        db: 데이터베이스 세션

    Returns:
        장기자랑 목록
    """
    repo = TalentRepository(db)
    if gender:
        talents = await repo.get_by_gender(gender)
    else:
        talents = await repo.get_all_talents()
    return talents


@app.post("/api/session/start", response_model=ParticipationResponse)
async def start_session(
    data: ParticipationCreate, db: AsyncSession = Depends(get_db)
):
    """
    새로운 참여 세션 시작

    Args:
        data: 세션 생성 데이터 (성별, 원본 이미지 경로, 동의 여부)
        db: 데이터베이스 세션

    Returns:
        생성된 참여 세션 정보
    """
    repo = ParticipationRepository(db)
    participation = await repo.create(
        gender=data.gender,
        original_image_path=data.original_image_path,
        consent_agreed=data.consent_agreed,
    )
    return participation


@app.get("/api/session/{uuid}", response_model=ParticipationResponse)
async def get_session_by_uuid(uuid: str, db: AsyncSession = Depends(get_db)):
    """
    UUID로 세션 조회 (다운로드 페이지용)

    Args:
        uuid: 다운로드 페이지 UUID
        db: 데이터베이스 세션

    Returns:
        참여 세션 정보
    """
    repo = ParticipationRepository(db)
    participation = await repo.get_by_uuid(uuid, load_relations=True)
    if not participation:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    return participation


@app.post("/api/print", response_model=PrintLogResponse)
async def create_print_log(
    data: PrintLogCreate, db: AsyncSession = Depends(get_db)
):
    """
    인쇄 기록 생성

    Args:
        data: 인쇄 기록 데이터 (participation_id, image_type)
        db: 데이터베이스 세션

    Returns:
        생성된 인쇄 기록
    """
    repo = PrintLogRepository(db)
    print_log = await repo.create_print_log(
        participation_id=data.participation_id, image_type=data.image_type
    )
    return print_log


@app.get("/api/statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """
    전체 통계 조회

    Args:
        db: 데이터베이스 세션

    Returns:
        인쇄 통계 및 세션 통계
    """
    print_log_repo = PrintLogRepository(db)
    participation_repo = ParticipationRepository(db)

    print_stats = await print_log_repo.get_print_statistics()
    recent_sessions = await participation_repo.get_recent_sessions(limit=5)

    return {
        "print_statistics": print_stats,
        "recent_sessions_count": len(recent_sessions),
    }


@app.post("/api/generate/profile")
async def generate_profile_image(file: UploadFile = File(...)):
    """
    프로필 이미지 생성 (모의 FaceFusion 실행)

    Args:
        file: 업로드된 사용자 사진

    Returns:
        생성된 프로필 이미지 URL
    """
    try:
        logger.info(f"프로필 이미지 생성 요청 받음: {file.filename}")

        # 파일 형식 검증
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="이미지 파일만 업로드 가능합니다."
            )

        # 파일 읽기
        image_data = await file.read()

        # 모의 FaceFusion 실행 (실제로는 이미지 복사만 수행)
        result_filename = await facefusion_service.generate_profile_image(
            image_data=image_data,
            original_filename=file.filename
        )

        # 이미지 URL 생성
        image_url = f"http://localhost:8000/images/{result_filename}"

        logger.info(f"프로필 이미지 생성 완료: {result_filename}")

        return JSONResponse({
            "success": True,
            "image_url": image_url,
            "filename": result_filename,
            "message": "프로필 이미지가 성공적으로 생성되었습니다."
        })

    except Exception as e:
        logger.error(f"프로필 이미지 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/talent")
async def generate_talent_image(file: UploadFile = File(...)):
    """
    탤런트쇼 이미지 생성 (모의 FaceFusion 실행)

    Args:
        file: 업로드된 사용자 사진

    Returns:
        생성된 탤런트쇼 이미지 URL
    """
    try:
        logger.info(f"탤런트쇼 이미지 생성 요청 받음: {file.filename}")

        # 파일 형식 검증
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="이미지 파일만 업로드 가능합니다."
            )

        # 파일 읽기
        image_data = await file.read()

        # 모의 FaceFusion 실행 (실제로는 이미지 복사만 수행)
        result_filename = await facefusion_service.generate_talent_image(
            image_data=image_data,
            original_filename=file.filename
        )

        # 이미지 URL 생성
        image_url = f"http://localhost:8000/images/{result_filename}"

        logger.info(f"탤런트쇼 이미지 생성 완료: {result_filename}")

        return JSONResponse({
            "success": True,
            "image_url": image_url,
            "filename": result_filename,
            "message": "탤런트쇼 이미지가 성공적으로 생성되었습니다."
        })

    except Exception as e:
        logger.error(f"탤런트쇼 이미지 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    logger.info("서버 시작 중...")
    logger.info("모의 FaceFusion 모드로 실행됩니다 (실제 AI 모델은 실행되지 않음)")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
