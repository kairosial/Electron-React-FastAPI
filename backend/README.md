# 나는솔로 키오스크 백엔드

FaceFusion 모의 실행을 통한 이미지 생성 API 서버

## 개요

이 백엔드는 **모의(Mock) FaceFusion 모드**로 동작합니다. 실제 AI 모델을 실행하지 않고, 업로드된 이미지를 그대로 저장하여 반환합니다. AI 처리 시간은 시뮬레이션됩니다.

### 주요 기능

- ✅ 이미지 업로드 및 저장
- ✅ AI 처리 시간 시뮬레이션 (3-5초)
- ✅ 생성된 이미지 다운로드 URL 제공
- ✅ CORS 설정 (프론트엔드 통신)
- ⚠️ **실제 FaceFusion은 실행되지 않음**

## 설치 방법

### 1. Python 가상환경 생성 (권장)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

## 실행 방법

### 방법 1: 스크립트 사용

```bash
./start.sh
```

### 방법 2: 직접 실행

```bash
python3 main.py
```

### 방법 3: Uvicorn 직접 실행

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API 엔드포인트

### 1. 서버 상태 확인

```
GET /
```

**응답:**

```json
{
  "message": "나는솔로 키오스크 백엔드 서버",
  "status": "running",
  "mode": "mock_facefusion"
}
```

### 2. 헬스 체크

```
GET /health
```

**응답:**

```json
{
  "status": "healthy"
}
```

### 3. 프로필 이미지 생성

```
POST /api/generate/profile
Content-Type: multipart/form-data
```

**요청:**

- `file`: 업로드할 이미지 파일 (JPEG, PNG 등)

**응답:**

```json
{
  "success": true,
  "image_url": "http://localhost:8000/images/profile_20250101_120000_abc123.jpg",
  "filename": "profile_20250101_120000_abc123.jpg",
  "message": "프로필 이미지가 성공적으로 생성되었습니다."
}
```

### 4. 탤런트쇼 이미지 생성

```
POST /api/generate/talent
Content-Type: multipart/form-data
```

**요청:**

- `file`: 업로드할 이미지 파일 (JPEG, PNG 등)

**응답:**

```json
{
  "success": true,
  "image_url": "http://localhost:8000/images/talent_20250101_120000_def456.jpg",
  "filename": "talent_20250101_120000_def456.jpg",
  "message": "탤런트쇼 이미지가 성공적으로 생성되었습니다."
}
```

### 5. 생성된 이미지 다운로드

```
GET /images/{filename}
```

## 디렉토리 구조

```
backend/
├── main.py                    # FastAPI 메인 애플리케이션
├── facefusion_service.py      # FaceFusion 모의 실행 서비스
├── requirements.txt           # Python 의존성
├── start.sh                   # 서버 시작 스크립트
└── README.md                  # 이 파일
```

## 실제 FaceFusion 적용 방법

현재는 모의 모드로 동작하며, 실제 FaceFusion을 적용하려면 다음 단계를 따르세요:

### 1. FaceFusion 설치

```bash
# FaceFusion GitHub 저장소 클론
git clone https://github.com/facefusion/facefusion.git ../facefusion
cd ../facefusion

# FaceFusion 의존성 설치
pip install -r requirements.txt

# 필요한 AI 모델 다운로드
python download.py
```

### 2. 타겟 이미지 준비

```bash
# 프로필용 이미지 디렉토리 생성
mkdir -p ../assets/profile_targets

# 탤런트쇼용 이미지 디렉토리 생성
mkdir -p ../assets/talent_targets

# "나는솔로" 출연진 이미지 추가
# (저작권 주의!)
```

### 3. facefusion_service.py 수정

`facefusion_service.py` 파일 내부의 주석을 참고하여 실제 FaceFusion API를 호출하도록 코드를 수정하세요.

주요 변경사항:

- `asyncio.sleep()` 제거
- FaceFusion 라이브러리 import
- `generate_profile_image()` 및 `generate_talent_image()` 함수에서 실제 얼굴 합성 수행

### 4. requirements.txt 업데이트

```bash
# FaceFusion 의존성 추가
echo "facefusion" >> requirements.txt
pip install -r requirements.txt
```

## 개발 팁

### 로그 확인

서버 실행 시 콘솔에서 다음과 같은 로그를 확인할 수 있습니다:

```
INFO:     프로필 이미지 생성 요청 받음: captured_image.jpg
INFO:     AI 처리 시뮬레이션 중... (3.5초 대기)
INFO:     프로필 이미지 생성 완료 (모의): profile_20250101_120000_abc123.jpg
INFO:     ⚠️  실제 FaceFusion은 실행되지 않았습니다. 원본 이미지가 저장되었습니다.
```

### 포트 변경

다른 포트에서 실행하려면 `main.py`의 마지막 부분을 수정하세요:

```python
uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
```

프론트엔드의 `frontend/src/services/api.js`도 함께 수정해야 합니다:

```javascript
const API_BASE_URL = 'http://localhost:9000'
```

### CORS 오류 해결

프론트엔드가 다른 포트나 도메인에서 실행되는 경우, `main.py`의 CORS 설정에 해당 주소를 추가하세요:

```python
allow_origins=[
    "http://localhost:5173",
    "http://your-frontend-url:port",  # 추가
],
```

## 트러블슈팅

### 문제: 서버가 시작되지 않음

**해결:**

```bash
# 포트 8000이 이미 사용 중인지 확인
lsof -i :8000

# 사용 중인 프로세스 종료
kill -9 <PID>
```

### 문제: 모듈을 찾을 수 없음 (ModuleNotFoundError)

**해결:**

```bash
# 가상환경 활성화 확인
source venv/bin/activate

# 의존성 재설치
pip install -r requirements.txt
```

### 문제: 이미지가 저장되지 않음

**해결:**

```bash
# output 디렉토리 권한 확인
chmod 755 ../output

# 디렉토리가 없으면 생성
mkdir -p ../output
```

## 라이선스

이 프로젝트는 교육 및 프로토타입 목적으로 제작되었습니다.
