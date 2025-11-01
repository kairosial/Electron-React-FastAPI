# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ELECTRON DESKTOP APP                         │
│                          (Fullscreen Kiosk)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    REACT FRONTEND                              │  │
│  │                  (Vite + React 18)                             │  │
│  ├───────────────────────────────────────────────────────────────┤  │
│  │                                                                 │  │
│  │  Screen Flow:                                                  │  │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐      │  │
│  │  │ Consent │ → │ Camera  │ → │ Loading │ → │ Profile  │      │  │
│  │  │ Screen  │   │ Screen  │   │ Screen  │   │ Result   │      │  │
│  │  └─────────┘   └─────────┘   └─────────┘   └──────────┘      │  │
│  │                                    ↓            ↓              │  │
│  │                              ┌─────────┐   ┌──────────┐       │  │
│  │                              │ Loading │ → │ Talent   │       │  │
│  │                              │ Screen  │   │ Result   │       │  │
│  │                              └─────────┘   └──────────┘       │  │
│  │                                                 ↓              │  │
│  │                                    ┌────────────────┐          │  │
│  │                                    │ Reset to Start │          │  │
│  │                                    └────────────────┘          │  │
│  │                                                                 │  │
│  ├───────────────────────────────────────────────────────────────┤  │
│  │                                                                 │  │
│  │  Components:                                                   │  │
│  │  • ConsentScreen.jsx     - 개인정보 동의                       │  │
│  │  • CameraScreen.jsx      - 웹캠 촬영 (react-webcam)            │  │
│  │  • LoadingScreen.jsx     - AI 처리 대기                        │  │
│  │  • ProfileResultScreen   - 프로필 결과 + QR 코드               │  │
│  │  • TalentResultScreen    - 탤런트쇼 결과 + QR 코드             │  │
│  │                                                                 │  │
│  │  Services:                                                     │  │
│  │  • api.js               - 백엔드 API 통신                      │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP (localhost:5173 → 8000)
                                  │ CORS Enabled
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                       FASTAPI BACKEND                                │
│                    (Python + Uvicorn)                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  REST API Endpoints:                                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ GET  /                  - 서버 상태                            │  │
│  │ GET  /health            - 헬스 체크                            │  │
│  │ POST /api/generate/profile  - 프로필 이미지 생성              │  │
│  │ POST /api/generate/talent   - 탤런트쇼 이미지 생성            │  │
│  │ GET  /images/{filename} - 이미지 다운로드 (정적 파일 서빙)    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Services:                                                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  FaceFusionService (facefusion_service.py)                     │  │
│  │                                                                 │  │
│  │  • generate_profile_image()                                    │  │
│  │    - 3.5초 딜레이 시뮬레이션                                   │  │
│  │    - 이미지 저장 (원본 그대로)                                 │  │
│  │    - 고유 파일명 생성 (타임스탬프 + UUID)                      │  │
│  │                                                                 │  │
│  │  • generate_talent_image()                                     │  │
│  │    - 4.5초 딜레이 시뮬레이션                                   │  │
│  │    - 이미지 저장 (원본 그대로)                                 │  │
│  │    - 고유 파일명 생성                                          │  │
│  │                                                                 │  │
│  │  • cleanup_old_files()                                         │  │
│  │    - 24시간 이상 된 파일 자동 삭제                             │  │
│  │                                                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ File I/O
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         FILE SYSTEM                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  output/                                                             │
│  ├── profile_20250101_120530_a3b5c7d9.jpg                           │
│  ├── talent_20250101_120545_b8c3d1e4.jpg                            │
│  └── ...                                                             │
│                                                                       │
│  assets/ (실제 FaceFusion 적용 시 사용)                              │
│  ├── profile_targets/                                                │
│  │   ├── contestant_1.jpg                                           │
│  │   └── ...                                                         │
│  └── talent_targets/                                                 │
│      ├── performer_1.jpg                                             │
│      └── ...                                                         │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow (Image Processing)

```
┌─────────────┐
│   USER      │
│ (Webcam)    │
└──────┬──────┘
       │
       │ 1. Capture Image
       ↓
┌──────────────────────────────────────────┐
│  CameraScreen.jsx                         │
│  - react-webcam.getScreenshot()          │
│  - Returns: base64 image data            │
└──────┬───────────────────────────────────┘
       │
       │ 2. Call handleCapture(imageSrc)
       ↓
┌──────────────────────────────────────────┐
│  App.jsx                                  │
│  - setCapturedImage(imageSrc)            │
│  - setCurrentScreen(3) // Loading        │
└──────┬───────────────────────────────────┘
       │
       │ 3. API Call
       ↓
┌──────────────────────────────────────────┐
│  api.js                                   │
│  - generateProfileImage(imageSrc)        │
│  - base64ToBlob()                        │
│  - FormData with file blob              │
└──────┬───────────────────────────────────┘
       │
       │ 4. HTTP POST Request
       │    Content-Type: multipart/form-data
       │
       ↓
┌──────────────────────────────────────────┐
│  Backend: main.py                         │
│  POST /api/generate/profile              │
│  - Validate file type                    │
│  - Read file data                        │
└──────┬───────────────────────────────────┘
       │
       │ 5. Call Service
       ↓
┌──────────────────────────────────────────┐
│  facefusion_service.py                   │
│  - generate_profile_image()              │
│                                           │
│  Mock Processing:                        │
│  • await asyncio.sleep(3.5)              │
│  • Generate unique filename              │
│  • Save image to output/                 │
│  • Return filename                       │
│                                           │
│  Real FaceFusion (Future):               │
│  • Load source image                     │
│  • Select random target image            │
│  • FaceFusion.swap_face()                │
│  • Save result to output/                │
│  • Return filename                       │
└──────┬───────────────────────────────────┘
       │
       │ 6. Return Response
       ↓
┌──────────────────────────────────────────┐
│  Backend: main.py                         │
│  Response JSON:                          │
│  {                                        │
│    "success": true,                      │
│    "image_url": "http://...",            │
│    "filename": "profile_xxx.jpg"         │
│  }                                       │
└──────┬───────────────────────────────────┘
       │
       │ 7. HTTP Response
       ↓
┌──────────────────────────────────────────┐
│  api.js                                   │
│  - Receive response                      │
│  - Extract image_url                     │
│  - Return { imageUrl, filename }         │
└──────┬───────────────────────────────────┘
       │
       │ 8. Update UI
       ↓
┌──────────────────────────────────────────┐
│  App.jsx                                  │
│  - setProfileImageUrl(result.imageUrl)  │
│  - setCurrentScreen(4) // Show result   │
└──────┬───────────────────────────────────┘
       │
       │ 9. Display Result
       ↓
┌──────────────────────────────────────────┐
│  ProfileResultScreen.jsx                  │
│  - <img src={imageUrl} />                │
│  - <QRCode value={imageUrl} />           │
│  - Download button                       │
└──────────────────────────────────────────┘
       │
       │ 10. User scans QR or clicks Next
       ↓
   [Repeat for Talent Generation]
```

---

## Technology Stack

### Frontend

```
Electron 33.2.0
    ↓
┌──────────────────────────────────────┐
│  React 18.3.1                         │
│  ├── Functional Components           │
│  ├── Hooks (useState)                │
│  └── Conditional Rendering           │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Build Tool: Vite 5.4.11             │
│  ├── Fast HMR                        │
│  ├── ES Modules                      │
│  └── Optimized Build                 │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Key Libraries                        │
│  ├── react-webcam 7.2.0              │
│  ├── qrcode.react 4.1.0              │
│  └── electron-builder 25.1.8         │
└──────────────────────────────────────┘
```

### Backend

```
Python 3.8+
    ↓
┌──────────────────────────────────────┐
│  FastAPI 0.104.1                     │
│  ├── Auto API Documentation          │
│  ├── Type Hints                      │
│  ├── Async/Await Support             │
│  └── Pydantic Validation             │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  ASGI Server: Uvicorn 0.24.0         │
│  ├── Auto Reload (Dev)               │
│  ├── Worker Processes                │
│  └── WebSocket Support               │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Middleware                           │
│  ├── CORS                            │
│  ├── Static Files                   │
│  └── Exception Handlers              │
└──────────────────────────────────────┘
```

---

## File Structure

```
Electron-React-FastAPI/
│
├─── FRONTEND LAYER ───────────────────────────────────────
│   frontend/
│   ├── electron/
│   │   └── main.js              # Electron main process
│   ├── src/
│   │   ├── components/          # React UI components
│   │   │   ├── ConsentScreen.jsx
│   │   │   ├── CameraScreen.jsx
│   │   │   ├── LoadingScreen.jsx
│   │   │   ├── ProfileResultScreen.jsx
│   │   │   └── TalentResultScreen.jsx
│   │   ├── services/            # Business logic
│   │   │   └── api.js           # Backend API client
│   │   ├── App.jsx              # Root component
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├─── BACKEND LAYER ────────────────────────────────────────
│   backend/
│   ├── main.py                  # FastAPI application
│   ├── facefusion_service.py    # Image processing logic
│   ├── requirements.txt         # Python dependencies
│   ├── start.sh                 # Startup script
│   └── README.md                # Backend documentation
│
├─── DATA LAYER ───────────────────────────────────────────
│   output/                      # Generated images
│   │   ├── profile_*.jpg
│   │   └── talent_*.jpg
│   │
│   assets/                      # Source images (future)
│   │   ├── profile_targets/
│   │   └── talent_targets/
│
├─── DOCUMENTATION ────────────────────────────────────────
│   ├── README.md                # Main project docs
│   ├── ARCHITECTURE.md          # This file
│   ├── IMPLEMENTATION_SUMMARY.md # Implementation details
│   ├── CLAUDE.md                # Development guidelines
│   └── .gitignore
│
└─── CONFIGURATION ────────────────────────────────────────
    └── .claude/
        └── settings.local.json
```

---

## API Specification

### POST /api/generate/profile

**Request:**
```http
POST /api/generate/profile HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="captured_image.jpg"
Content-Type: image/jpeg

[binary image data]
------WebKitFormBoundary--
```

**Response (Success):**
```json
{
  "success": true,
  "image_url": "http://localhost:8000/images/profile_20250101_120530_a3b5c7d9.jpg",
  "filename": "profile_20250101_120530_a3b5c7d9.jpg",
  "message": "프로필 이미지가 성공적으로 생성되었습니다."
}
```

**Response (Error):**
```json
{
  "detail": "이미지 파일만 업로드 가능합니다."
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Invalid file type
- `500 Internal Server Error` - Processing failed

---

### POST /api/generate/talent

(Same structure as `/api/generate/profile`)

---

### GET /images/{filename}

**Request:**
```http
GET /images/profile_20250101_120530_a3b5c7d9.jpg HTTP/1.1
Host: localhost:8000
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Length: 123456

[binary image data]
```

---

## Mock vs Real FaceFusion

### Current Implementation (Mock)

```python
async def generate_profile_image(image_data, filename):
    # Simulate AI processing time
    await asyncio.sleep(3.5)

    # Save original image as-is
    output_path = output_dir / f"profile_{timestamp}_{uuid}.jpg"
    with open(output_path, "wb") as f:
        f.write(image_data)

    return filename
```

**Characteristics:**
- ✅ Fast development
- ✅ No GPU required
- ✅ Predictable results
- ⚠️ No actual face swapping

---

### Future Implementation (Real)

```python
async def generate_profile_image(image_data, filename):
    # Save source image
    source_path = save_temp_image(image_data)

    # Select random target
    target_path = random.choice(profile_targets)

    # Run FaceFusion
    facefusion = FaceFusion()
    result_path = await facefusion.swap_face(
        source=source_path,
        target=target_path,
        output=output_path,
        face_enhancer="gfpgan",
        face_detector="retinaface"
    )

    # Cleanup temp files
    cleanup_temp(source_path)

    return filename
```

**Requirements:**
- GPU (NVIDIA recommended)
- CUDA/cuDNN
- 4-8GB VRAM
- FaceFusion models (~2GB)
- Target images (celebrities, "나는 솔로" cast)

---

## Security Considerations

### Current Implementation

✅ **File Type Validation**
```python
if not file.content_type.startswith("image/"):
    raise HTTPException(status_code=400, ...)
```

✅ **CORS Restrictions**
```python
allow_origins=["http://localhost:5173"]
```

✅ **Unique Filenames**
```python
filename = f"profile_{timestamp}_{uuid.uuid4()[:8]}.jpg"
```

### Future Enhancements

⚠️ **To Add:**
- File size limits (prevent DoS)
- Rate limiting (prevent abuse)
- Image content validation (detect inappropriate content)
- HTTPS for production
- Authentication/authorization
- Input sanitization
- SQL injection prevention (if using DB)

---

## Performance Optimization

### Current Performance

**Mock Mode:**
- Profile generation: 3.5 seconds
- Talent generation: 4.5 seconds
- File upload: < 100ms
- Image serving: < 50ms

### Real FaceFusion Performance

**Expected:**
- GPU (RTX 3060): 5-10 seconds/image
- GPU (RTX 4090): 2-5 seconds/image
- CPU only: 30-60 seconds/image

**Optimization Strategies:**
1. GPU acceleration (CUDA)
2. Model caching (load once)
3. Batch processing
4. Result caching (same source + target)
5. Image preprocessing (resize, normalize)
6. Queue system (Redis + Celery)

---

## Deployment Architecture (Future)

```
┌─────────────────┐
│   LOAD          │
│   BALANCER      │
│   (Nginx)       │
└────────┬────────┘
         │
         ├───────────┬───────────┐
         ↓           ↓           ↓
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Frontend   │ │ Frontend   │ │ Frontend   │
│ Instance 1 │ │ Instance 2 │ │ Instance 3 │
└────────────┘ └────────────┘ └────────────┘
         │           │           │
         └───────────┴───────────┘
                     ↓
         ┌───────────────────────┐
         │   API Gateway         │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
┌────────────────┐      ┌────────────────┐
│ Backend API 1  │      │ Backend API 2  │
│ (FastAPI)      │      │ (FastAPI)      │
└────────┬───────┘      └────────┬───────┘
         │                       │
         └───────────┬───────────┘
                     ↓
         ┌───────────────────────┐
         │ Task Queue (Redis)    │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
┌────────────────┐      ┌────────────────┐
│ Worker 1       │      │ Worker 2       │
│ (FaceFusion)   │      │ (FaceFusion)   │
│ GPU Required   │      │ GPU Required   │
└────────┬───────┘      └────────┬───────┘
         │                       │
         └───────────┬───────────┘
                     ↓
         ┌───────────────────────┐
         │ Storage (S3/MinIO)    │
         │ - Source images       │
         │ - Generated images    │
         │ - Target images       │
         └───────────────────────┘
```

---

## Summary

이 아키텍처는 **완전한 E2E 워크플로우**를 제공하며, 실제 FaceFusion으로 쉽게 전환 가능한 **확장 가능한 구조**를 가지고 있습니다.

**핵심 설계 원칙:**
1. **모듈화** - 각 레이어가 독립적으로 동작
2. **확장성** - 실제 AI 모델 적용 시 최소 변경
3. **개발자 친화적** - 명확한 구조와 문서
4. **사용자 중심** - 빠른 응답과 에러 핸들링
