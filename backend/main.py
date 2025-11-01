"""
나는솔로 키오스크 백엔드 서버
FaceFusion 모의 실행 API
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import logging

from facefusion_service import FaceFusionService

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
