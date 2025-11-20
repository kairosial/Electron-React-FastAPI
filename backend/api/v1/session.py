"""
Session API Routes

세션 관리 관련 5개 엔드포인트를 제공합니다.
"""

from fastapi import APIRouter, Depends, status, UploadFile, File
from pydantic import BaseModel

from backend.services.session_service import SessionService
from backend.core.dependencies import get_session_service
from backend.utils.response import create_success_response

router = APIRouter(prefix="/session")


# Request/Response Models
class SessionStartRequest(BaseModel):
    """세션 시작 요청"""
    consent_agreed: bool


class GenderUpdateRequest(BaseModel):
    """성별 업데이트 요청"""
    gender: str


# 1. POST /session/start - 세션 시작 (화면 #2)
@router.post("/start", status_code=status.HTTP_201_CREATED)
async def start_session(
    request: SessionStartRequest,
    service: SessionService = Depends(get_session_service)
):
    """
    새로운 참여 세션 시작

    - **consent_agreed**: 개인정보 수집 동의 (true 필수)
    """
    session = await service.create_session(request.consent_agreed)
    return create_success_response(
        data=session,
        message="Session started successfully"
    )


# 2. PATCH /session/{participation_id}/gender - 성별 업데이트 (화면 #3)
@router.patch("/{participation_id}/gender")
async def update_gender(
    participation_id: int,
    request: GenderUpdateRequest,
    service: SessionService = Depends(get_session_service)
):
    """
    성별 선택

    - **participation_id**: 참여 ID
    - **gender**: 성별 ('male' 또는 'female')
    """
    result = await service.update_gender(participation_id, request.gender)
    return create_success_response(
        data=result,
        message="Gender updated successfully"
    )


# 3. POST /session/{participation_id}/upload-image - 이미지 업로드 (화면 #4)
@router.post("/{participation_id}/upload-image")
async def upload_image(
    participation_id: int,
    image: UploadFile = File(...),
    service: SessionService = Depends(get_session_service)
):
    """
    원본 이미지 업로드

    - **participation_id**: 참여 ID
    - **image**: 업로드할 이미지 파일 (jpg, jpeg, png)
    """
    result = await service.upload_image(participation_id, image)
    return create_success_response(
        data=result,
        message="Image uploaded successfully"
    )


# 4. GET /session/{participation_id}/result - 결과 조회 (화면 #7-1, #9-1)
@router.get("/{participation_id}/result")
async def get_result(
    participation_id: int,
    service: SessionService = Depends(get_session_service)
):
    """
    생성된 이미지 및 메타데이터 조회

    - **participation_id**: 참여 ID
    """
    result = await service.get_result(participation_id)
    return create_success_response(
        data=result,
        message="Result retrieved successfully"
    )


# 5. GET /session/{uuid} - UUID로 세션 조회 (화면 #7-2, #9-2)
@router.get("/{uuid}")
async def get_session_by_uuid(
    uuid: str,
    service: SessionService = Depends(get_session_service)
):
    """
    다운로드 페이지용 세션 조회

    - **uuid**: 다운로드 페이지 UUID
    """
    result = await service.get_by_uuid(uuid)
    return create_success_response(
        data=result,
        message="Session retrieved successfully"
    )
