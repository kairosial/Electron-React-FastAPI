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
echo "⚠️  모의 FaceFusion 모드로 실행됩니다"
echo "실제 AI 모델은 실행되지 않으며, 업로드된 이미지가 그대로 반환됩니다."
echo ""

# 가상환경 활성화 (있다면)
if [ -d "venv" ]; then
    echo "가상환경 활성화 중..."
    source venv/bin/activate
fi

# 백엔드 디렉토리로 이동
cd "$(dirname "$0")"

# 서버 실행
echo "서버 시작 중... (http://localhost:8000)"
echo ""
python3 main.py
