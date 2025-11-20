"""
API v1 router aggregator

모든 v1 라우터를 집계하여 하나의 APIRouter로 제공합니다.
"""

from fastapi import APIRouter

from backend.api.v1 import session, image, target, tracking, print_router, dashboard

# API Router 생성
api_router = APIRouter()

# 각 도메인 라우터 등록
api_router.include_router(session.router, tags=["Session"])
api_router.include_router(image.router, tags=["Image"])
api_router.include_router(target.router, tags=["Target"])
api_router.include_router(tracking.router, tags=["Tracking"])
api_router.include_router(print_router.router, tags=["Print"])
api_router.include_router(dashboard.router, tags=["Dashboard"])
