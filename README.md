# 나는솔로 키오스크 (Electron-React-FastAPI)

"나는 솔로" 팝업 스토어를 위한 인터랙티브 키오스크 애플리케이션

## 프로젝트 개요

사용자가 웹캠으로 사진을 촬영하면, FaceFusion AI를 통해 "나는 솔로" 출연진 스타일의 프로필 사진과 탤런트쇼 이미지를 생성하는 키오스크 앱입니다.

### 주요 기능

- 📸 웹캠을 통한 실시간 사진 촬영
- 🎭 AI 기반 얼굴 합성 (FaceFusion)
- ✨ 프로필 이미지 및 탤런트쇼 이미지 생성
- 📱 QR 코드를 통한 이미지 다운로드
- 🖥️ Electron 기반 전체화면 키오스크 모드

### 현재 상태

⚠️ **모의(Mock) FaceFusion 모드로 동작**

실제 FaceFusion AI 모델은 실행되지 않으며, 업로드된 이미지를 그대로 반환합니다. AI 처리 시간(3-5초)만 시뮬레이션됩니다.

## 기술 스택

### Frontend
- **Electron** 33.2.0 - 데스크톱 앱 런타임
- **React** 18.3.1 - UI 프레임워크
- **Vite** 5.4.11 - 빌드 도구
- **react-webcam** 7.2.0 - 웹캠 캡처
- **qrcode.react** 4.1.0 - QR 코드 생성

### Backend
- **FastAPI** 0.104.1 - Python 웹 프레임워크
- **Uvicorn** 0.24.0 - ASGI 서버
- **FaceFusion** (예정) - AI 얼굴 합성

## 설치 및 실행

### 전제 조건

- Node.js 18 이상
- Python 3.8 이상
- npm 또는 yarn

### 1. 프로젝트 클론

```bash
git clone https://github.com/your-username/Electron-React-FastAPI.git
cd Electron-React-FastAPI
```

### 2. 백엔드 설정

```bash
cd backend

# Python 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python3 main.py
# 또는
./start.sh
```

백엔드는 `http://localhost:8000`에서 실행됩니다.

### 3. 프론트엔드 설정

새 터미널을 열어서:

```bash
cd frontend

# 의존성 설치
npm install

# 개발 모드 실행 (브라우저)
npm run dev

# 또는 Electron 앱으로 실행
npm run electron:dev
```

프론트엔드는 `http://localhost:5173`에서 실행됩니다.

### 4. 프로덕션 빌드

```bash
cd frontend

# Vite 빌드
npm run build

# Electron 배포 파일 생성
npm run electron:build
```

빌드된 앱은 `frontend/release/` 디렉토리에 생성됩니다.

## 프로젝트 구조

```
Electron-React-FastAPI/
├── frontend/                   # Electron + React 프론트엔드
│   ├── electron/              # Electron 메인 프로세스
│   │   └── main.js
│   ├── src/
│   │   ├── components/        # React 컴포넌트
│   │   │   ├── ConsentScreen.jsx
│   │   │   ├── CameraScreen.jsx
│   │   │   ├── LoadingScreen.jsx
│   │   │   ├── ProfileResultScreen.jsx
│   │   │   └── TalentResultScreen.jsx
│   │   ├── services/          # API 통신 서비스
│   │   │   └── api.js
│   │   ├── App.jsx            # 메인 앱 컴포넌트
│   │   ├── main.jsx           # React 엔트리포인트
│   │   └── index.css          # 글로벌 스타일
│   ├── package.json
│   └── vite.config.js
│
├── backend/                    # FastAPI 백엔드
│   ├── main.py                # FastAPI 메인 앱
│   ├── facefusion_service.py  # FaceFusion 모의 실행 서비스
│   ├── requirements.txt       # Python 의존성
│   ├── start.sh              # 서버 시작 스크립트
│   └── README.md             # 백엔드 문서
│
├── output/                     # 생성된 이미지 저장
├── assets/                     # 미디어 리소스 (타겟 이미지 등)
├── facefusion/                 # FaceFusion 통합 (예정)
├── docs/                       # 프로젝트 문서
└── README.md                   # 이 파일
```

## 사용 흐름

1. **동의서 화면** - 사용자가 개인정보 수집 동의
2. **촬영 화면** - 웹캠으로 사진 촬영
3. **로딩 화면** - AI 처리 중 (3.5초 시뮬레이션)
4. **프로필 결과 화면** - 생성된 프로필 이미지 표시 + QR 코드
5. **탤런트쇼 생성** - "다음" 버튼 클릭
6. **로딩 화면** - AI 처리 중 (4.5초 시뮬레이션)
7. **탤런트쇼 결과 화면** - 생성된 탤런트쇼 이미지 표시 + QR 코드
8. **처음으로** - 다시 동의서 화면으로

## API 문서

백엔드 서버 실행 후 다음 주소에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 실제 FaceFusion 적용 방법

현재는 모의 모드로 동작합니다. 실제 FaceFusion을 적용하려면 [backend/README.md](backend/README.md)의 "실제 FaceFusion 적용 방법" 섹션을 참조하세요.

주요 단계:
1. FaceFusion 라이브러리 설치
2. AI 모델 다운로드
3. 타겟 이미지 준비 ("나는 솔로" 출연진 이미지)
4. `facefusion_service.py` 코드 수정
5. 실제 얼굴 합성 로직 구현

## 개발 가이드

### 백엔드 개발

```bash
cd backend

# 가상환경 활성화
source venv/bin/activate

# 서버 실행 (자동 리로드)
uvicorn main:app --reload

# 새 엔드포인트 추가 시 main.py 수정
# API 문서 자동 업데이트: http://localhost:8000/docs
```

### 프론트엔드 개발

```bash
cd frontend

# 개발 서버 실행 (HMR 지원)
npm run dev

# Electron 앱으로 테스트
npm run electron:dev

# 컴포넌트 수정 시 src/components/ 디렉토리 참조
# API 호출 추가 시 src/services/api.js 수정
```

### 스타일 수정

- 글로벌 스타일: `frontend/src/index.css`
- 색상 테마: 보라색 그라디언트 (`#667eea` → `#764ba2`)
- 레이아웃: Flexbox 기반

## 트러블슈팅

### 백엔드 서버가 시작되지 않음

```bash
# 포트 8000 확인
lsof -i :8000

# 의존성 재설치
pip install -r requirements.txt
```

### 프론트엔드가 백엔드에 연결되지 않음

1. 백엔드가 실행 중인지 확인: `http://localhost:8000/health`
2. CORS 설정 확인: `backend/main.py`의 `allow_origins`
3. API URL 확인: `frontend/src/services/api.js`의 `API_BASE_URL`

### Electron 앱이 실행되지 않음

```bash
cd frontend

# 의존성 재설치
rm -rf node_modules package-lock.json
npm install

# 캐시 정리
npm run clean  # (필요시 package.json에 스크립트 추가)
```

## 라이선스

이 프로젝트는 교육 및 프로토타입 목적으로 제작되었습니다.

## 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 참고 자료

- [FaceFusion GitHub](https://github.com/facefusion/facefusion)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [React 문서](https://react.dev/)
- [Electron 문서](https://www.electronjs.org/)
