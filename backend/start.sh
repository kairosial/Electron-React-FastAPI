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

# FaceFusion 라이브러리 경로 추가
export PYTHONPATH="/Users/syk/PC/git/facefusion:$PYTHONPATH"
echo "FaceFusion 경로 설정: /Users/syk/PC/git/facefusion"

# 백엔드 디렉토리로 이동
cd "$(dirname "$0")"

# .env 파일 로드
if [ -f ".env" ]; then
    echo ".env 파일 로드됨"
    export $(cat .env | grep -v '^#' | xargs)
fi

# 서버 실행 (Poetry 환경 사용)
echo "서버 시작 중... (http://localhost:8000)"
echo ""
cd ..
poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
