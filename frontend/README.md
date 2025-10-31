# 나는 솔로 키오스크 - 프론트엔드 프로토타입

"나는 솔로" 팝업스토어 체험 키오스크의 프론트엔드 애플리케이션입니다.

## 기술 스택

- **Electron**: 데스크톱 애플리케이션 (키오스크 전체화면 모드)
- **React 18**: UI 컴포넌트
- **Vite**: 빠른 개발 서버 및 빌드
- **react-webcam**: 웹캠 촬영 기능
- **qrcode.react**: QR 코드 생성

## 프로젝트 구조

```
frontend/
├── electron/
│   └── main.js              # Electron 메인 프로세스
├── src/
│   ├── components/          # React 컴포넌트
│   │   ├── ConsentScreen.jsx       # 1. 동의서 화면
│   │   ├── CameraScreen.jsx        # 2. 웹캠 촬영 화면
│   │   ├── LoadingScreen.jsx       # 3. AI 처리 중 로딩 화면
│   │   ├── ProfileResultScreen.jsx # 4. 프로필 결과 화면
│   │   └── TalentResultScreen.jsx  # 5. 장기자랑 결과 화면
│   ├── App.jsx              # 메인 앱 (화면 전환 로직)
│   ├── main.jsx             # React 진입점
│   └── index.css            # 스타일
├── index.html
├── vite.config.js
└── package.json
```

## 설치 및 실행

### 1. 의존성 설치

```bash
cd frontend
npm install
```

### 2. 개발 모드 실행 (브라우저)

웹 브라우저에서 빠르게 테스트하려면:

```bash
npm run dev
```

그 다음 브라우저에서 http://localhost:5173 접속

### 3. Electron 모드 실행 (키오스크)

Electron 앱으로 실행하려면:

```bash
npm run electron:dev
```

자동으로 Electron 창이 열리며 전체화면(풀스크린)으로 실행됩니다.

### 4. 프로덕션 빌드

```bash
npm run electron:build
```

`release/` 폴더에 실행 파일이 생성됩니다.

## 화면 플로우

```
1. 동의서 화면 (ConsentScreen)
   ↓ (모두 동의)
2. 촬영 화면 (CameraScreen)
   ↓ (사진 촬영 및 확인)
3. 로딩 화면 (LoadingScreen)
   ↓ (AI 처리 3초)
4. 프로필 결과 화면 (ProfileResultScreen)
   ↓ (계속 진행 선택)
3. 로딩 화면 (LoadingScreen)
   ↓ (AI 처리 3초)
5. 장기자랑 결과 화면 (TalentResultScreen)
   ↓ (처음으로)
1. 동의서 화면으로 돌아감
```

## 주요 기능

### ✅ 구현 완료

- [x] 5개 화면 컴포넌트
- [x] 화면 전환 로직 (useState 기반)
- [x] 웹캠 촬영 및 미리보기
- [x] 재촬영 기능
- [x] QR 코드 생성 및 표시
- [x] 전체화면 키오스크 모드

### 🔄 백엔드 연동 필요 (현재는 더미 데이터)

현재 프로토타입은 백엔드 없이 작동하며, 다음 부분을 나중에 연동해야 합니다:

1. **이미지 업로드** ([App.jsx:28](App.jsx#L28))
   ```javascript
   // TODO: 백엔드 API 호출
   const response = await fetch('http://localhost:8000/api/generate/profile', {
     method: 'POST',
     body: formData
   })
   ```

2. **AI 생성 이미지 받기** ([App.jsx:32](App.jsx#L32))
   ```javascript
   // TODO: 실제 생성된 이미지 URL 사용
   setProfileImageUrl(response.data.imageUrl)
   ```

3. **QR 코드 URL** ([ProfileResultScreen.jsx:6](ProfileResultScreen.jsx#L6))
   ```javascript
   // TODO: 백엔드에서 제공하는 이미지 호스팅 URL
   const downloadUrl = props.qrCodeUrl
   ```

## 개발 팁

### React 기초 이해하기

이 프로젝트는 React의 핵심 개념만 사용합니다:

1. **useState**: 화면 상태 관리
   ```javascript
   const [currentScreen, setCurrentScreen] = useState(1)
   ```

2. **props**: 부모 → 자식 데이터 전달
   ```javascript
   <ConsentScreen onAgree={handleConsentAgree} />
   ```

3. **조건부 렌더링**: 화면 전환
   ```javascript
   {currentScreen === 1 && <ConsentScreen />}
   ```

### 웹캠 테스트

웹캠이 작동하지 않으면:
- 브라우저/Electron에서 카메라 권한 허용 확인
- macOS: 시스템 환경설정 → 보안 및 개인정보보호 → 카메라

### 스타일 수정

[index.css](index.css)에서 모든 스타일을 수정할 수 있습니다:
- 색상 테마 변경: `.screen` 배경색
- 버튼 스타일: `.button` 클래스
- 레이아웃: flexbox 속성 조정

## 다음 단계

1. **백엔드 개발** (FastAPI + facefusion)
2. **API 연동**: fetch 또는 axios로 통신
3. **실제 디자인 적용**: 와이어프레임 나오면 CSS 교체
4. **에러 처리**: 웹캠 실패, 네트워크 오류 등

## 문제 해결

### npm install 실패
```bash
# Node.js 버전 확인 (18 이상 필요)
node --version

# npm 캐시 정리
npm cache clean --force
npm install
```

### Electron 창이 안 열림
```bash
# Vite 개발 서버가 먼저 실행되었는지 확인
npm run dev  # 별도 터미널에서 먼저 실행
npm run electron:dev  # 다른 터미널에서 실행
```

### 웹캠이 검은 화면
- 다른 앱에서 웹캠을 사용 중인지 확인
- 브라우저에서 카메라 권한 허용

## 참고 자료

- [React 공식 문서](https://react.dev/learn)
- [react-webcam GitHub](https://github.com/mozmorris/react-webcam)
- [Electron 공식 문서](https://www.electronjs.org/docs/latest)
