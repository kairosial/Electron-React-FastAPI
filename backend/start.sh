#!/bin/bash

# 나는솔로 키오스크 백엔드 시작 스크립트

echo "======================================"
echo "나는솔로 키오스크 백엔드 서버 시작"
echo "======================================"
echo ""

# Python 버전 확인
echo "Python 버전 확인 중..."
python3 --version

echo ""
echo "✅ FaceFusion 통합 모드로 실행됩니다"
echo "실제 AI 얼굴 합성이 수행됩니다."
echo ""

# 백엔드 디렉토리로 이동
cd "$(dirname "$0")"

# .env 파일 로드
if [ -f ".env" ]; then
    echo ".env 파일 로드 중..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# FaceFusion 경로 설정 (환경변수가 없으면 상대 경로 사용)
if [ -z "$FACEFUSION_PATH" ]; then
    SCRIPT_DIR="$(pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    FACEFUSION_PATH="$(cd "$PROJECT_ROOT/../facefusion" 2>/dev/null && pwd)"

    if [ -z "$FACEFUSION_PATH" ] || [ ! -f "$FACEFUSION_PATH/facefusion/__init__.py" ]; then
        echo "❌ FaceFusion을 찾을 수 없습니다!"
        echo "   다음 중 하나를 확인해주세요:"
        echo "   1. ../facefusion 경로에 FaceFusion 설치"
        echo "   2. backend/.env 파일에 FACEFUSION_PATH 설정"
        exit 1
    fi
fi

export PYTHONPATH="$FACEFUSION_PATH:$PYTHONPATH"
echo "✅ FaceFusion 경로: $FACEFUSION_PATH"

# 서버 실행 (Poetry 환경 사용)
echo "서버 시작 중... (http://localhost:8000)"
echo ""
cd ..
poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
