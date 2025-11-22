# FaceFusion 설정 가이드

이 문서는 실제 FaceFusion을 이용한 얼굴 합성 기능을 설정하는 방법을 설명합니다.

## 목차

1. [개요](#개요)
2. [사전 요구사항](#사전-요구사항)
3. [FaceFusion 설치](#facefusion-설치)
4. [프로젝트 설정](#프로젝트-설정)
5. [테스트](#테스트)
6. [문제 해결](#문제-해결)

---

## 개요

현재 프로젝트는 `../facefusion` 디렉토리에 있는 FaceFusion 프로젝트를 **직접 Python 모듈로 import**하여 얼굴 합성을 수행합니다.

**작동 방식:**
1. FastAPI 서버 시작 시 `facefusion` 경로를 `sys.path`에 추가
2. `FaceFusionService` 초기화 시 AI 모델을 메모리에 로드 (한 번만)
3. 요청마다 메모리에 로드된 모델을 재사용하여 빠르게 처리
4. Subprocess 방식이 아니므로 매번 모델을 다시 로드할 필요 없음

**성능 이점:**
- ✅ AI 모델을 한 번만 메모리에 로드
- ✅ 이후 요청은 즉시 처리 (모델 로드 시간 제거)
- ✅ 프로세스 생성 오버헤드 없음

---

## 사전 요구사항

### 1. Python 버전
- Python 3.10 이상 필수
- **중요:** 백엔드와 동일한 Python 환경 사용

```bash
python --version  # 3.10 이상이어야 함
```

### 2. FaceFusion 의존성
Poetry로 이미 추가되어 있습니다 (`pyproject.toml`):
- numpy >= 2.0.0
- onnx ^1.19.1
- onnxruntime ^1.23.2
- opencv-python ^4.12.0
- scipy ^1.13.0
- 기타 의존성들

### 3. 시스템 도구
- **curl**: 모델 다운로드에 필요
- **ffmpeg**: 이미지 처리에 필요

**macOS:**
```bash
brew install curl ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install curl ffmpeg
```

### 4. 하드웨어 권장사항
- **CPU 모드**: 최소 4코어, 8GB RAM
- **GPU 모드** (선택사항):
  - NVIDIA GPU: CUDA 11.8 이상
  - Apple Silicon: Metal 지원

---

## FaceFusion 설치

### 1. 의존성 설치

프로젝트 루트에서:

```bash
# Poetry로 모든 의존성 설치 (FaceFusion 포함)
poetry install

# 또는 poetry를 사용하지 않는 경우
pip install -r backend/requirements.txt
```

### 2. FaceFusion AI 모델 다운로드

FaceFusion 디렉토리에서 모델 다운로드:

```bash
cd /Users/syk/PC/git/facefusion

# 필요한 AI 모델 자동 다운로드
python facefusion.py force-download
```

**주요 다운로드 모델:**
- Face detector (YOLO)
- Face swapper (inswapper)
- Face landmarker
- Face recognizer

**다운로드 위치:** `/Users/syk/PC/git/facefusion/.assets/models/`

### 3. 설치 확인

```bash
cd /Users/syk/PC/git/facefusion
python facefusion.py --version
```

---

## 프로젝트 설정

### 1. 환경변수 설정

`backend/.env` 파일 (이미 설정됨):

```bash
# FaceFusion 모드
FACEFUSION_MODE=real  # 'real' 또는 'mock'

# FaceFusion 프로젝트 경로 (sys.path에 자동 추가)
FACEFUSION_PROJECT_PATH=../facefusion

# Face Swapper 모델
FACEFUSION_FACE_SWAPPER_MODEL=inswapper_128

# 실행 프로바이더
FACEFUSION_EXECUTION_PROVIDERS=cpu  # 또는 cuda,cpu / coreml,cpu
```

### 2. PYTHONPATH 설정 (선택사항)

`FaceFusionService`가 자동으로 `sys.path`에 추가하지만, 명시적으로 설정하려면:

```bash
# macOS/Linux
export PYTHONPATH="/Users/syk/PC/git/facefusion:$PYTHONPATH"

# 또는 .env 파일에
PYTHONPATH=/Users/syk/PC/git/facefusion
```

### 3. GPU 사용 설정 (선택사항)

**NVIDIA GPU (CUDA):**
```bash
FACEFUSION_EXECUTION_PROVIDERS=cuda,cpu
```

**Apple Silicon (M1/M2):**
```bash
FACEFUSION_EXECUTION_PROVIDERS=coreml,cpu
```

---

## 작동 원리

### 모듈 Import 방식

```python
# FaceFusionService 초기화 시
import sys
sys.path.insert(0, '/Users/syk/PC/git/facefusion')

from facefusion import state_manager
from facefusion.workflows import image_to_image

# state_manager에 50+ 설정 항목 초기화:
# - execution_providers, execution_device_ids, execution_thread_count
# - download_providers, download_scope
# - face_detector_model, face_detector_size, face_detector_score
# - face_landmarker_model, face_selector_mode
# - face_mask_types, face_mask_blur, face_mask_padding
# - face_swapper_model, face_swapper_pixel_boost, face_swapper_weight
# - output_image_quality, output_image_scale
# - temp_path, temp_frame_format, keep_temp
# - log_level, memory settings 등

# AI 모델은 처음 import 시 메모리에 로드됨 (1회만)
# 이후 모든 요청은 메모리에 로드된 모델 재사용
```

### 처리 플로우

```
서버 시작
  ↓
FaceFusionService.__init__()
  ↓
facefusion 모듈 import (sys.path 추가)
  ↓
AI 모델 메모리 로드 (1회)
  ↓
[서버 대기 - 모델은 메모리에 상주]
  ↓
API 요청: POST /session/{id}/generate-profile
  ↓
FaceFusionService.generate_image()
  ↓
state_manager.set_item(source, target, output)
  ↓
image_to_image.process() ← 메모리의 모델 재사용!
  ↓
얼굴 합성 완료 (빠름!)
```

---

## 테스트

### 1. 서버 시작 및 초기화 확인

```bash
cd /Users/syk/PC/git/Electron-React-FastAPI/backend

# 서버 시작 (로그 확인)
poetry run python -m uvicorn main:app --reload
```

**예상 로그:**
```
INFO: FaceFusion 서비스 초기화 완료
INFO: Mode: real
INFO: FaceFusion path: /Users/syk/PC/git/facefusion
INFO: FaceFusion 모듈 초기화 완료
INFO: FaceFusion 기본 설정 완료
```

### 2. API 테스트

```bash
# 1. 세션 시작
curl -X POST http://localhost:8000/api/v1/session/start \
  -H "Content-Type: application/json" \
  -d '{"consent_agreed": true}'

# 2. 성별 선택
curl -X PATCH http://localhost:8000/api/v1/session/1/gender \
  -H "Content-Type: application/json" \
  -d '{"gender": "male"}'

# 3. 이미지 업로드
curl -X POST http://localhost:8000/api/v1/session/1/upload-image \
  -F "image=@/path/to/photo.jpg"

# 4. 프로필 생성 (얼굴 합성!)
curl -X POST http://localhost:8000/api/v1/session/1/generate-profile
```

### 3. 성능 확인

첫 번째 요청:
```
INFO: Starting face fusion:
INFO:   Source: /path/to/source.jpg
INFO:   Target: /path/to/target.jpg
INFO:   Output: /path/to/output.jpg
INFO: Face fusion completed successfully in 15.23s
```

두 번째 요청 (모델 재사용):
```
INFO: Face fusion completed successfully in 8.45s  ← 훨씬 빠름!
```

---

## 문제 해결

### 1. "ModuleNotFoundError: No module named 'facefusion'"

**원인:** facefusion 경로가 잘못되었거나 모듈이 없음

**해결:**
```bash
# 1. facefusion 경로 확인
ls -la /Users/syk/PC/git/facefusion/facefusion

# 2. .env 파일에서 경로 확인
cat backend/.env | grep FACEFUSION_PROJECT_PATH

# 3. 절대 경로 사용
FACEFUSION_PROJECT_PATH=/Users/syk/PC/git/facefusion
```

### 2. "ImportError: cannot import name 'state_manager'"

**원인:** facefusion 의존성이 설치되지 않음

**해결:**
```bash
cd /Users/syk/PC/git/facefusion
pip install -r requirements.txt
```

### 3. AI 모델 로드 실패

**원인:** 모델 파일이 다운로드되지 않음

**해결:**
```bash
cd /Users/syk/PC/git/facefusion
python facefusion.py force-download

# 모델 확인
ls -la .assets/models/
```

### 4. 메모리 부족

**원인:** AI 모델이 너무 큼 (여러 모델 로드 시)

**해결:**
- 더 작은 모델 사용: `inswapper_128` → `inswapper_128_fp16`
- 서버 메모리 증가
- Docker 메모리 제한 증가

### 5. GPU 사용 오류

**CUDA 오류:**
```bash
# CPU로 전환
FACEFUSION_EXECUTION_PROVIDERS=cpu
```

**Apple Silicon 오류:**
```bash
# CoreML이 작동하지 않으면 CPU 사용
FACEFUSION_EXECUTION_PROVIDERS=cpu
```

---

## 성능 최적화

### 모델 선택

| 모델 | 크기 | 속도 | 품질 |
|-----|------|------|------|
| inswapper_128 | 중간 | 빠름 | 우수 (권장) |
| inswapper_128_fp16 | 작음 | 매우 빠름 | 우수 |
| blendswap_256 | 큼 | 느림 | 최고 |

### 실행 환경별 성능

**CPU 모드:**
- 첫 요청: ~15-20초 (모델 로드 포함)
- 이후 요청: ~8-12초 (모델 재사용)

**GPU 모드 (NVIDIA):**
- 첫 요청: ~5-8초
- 이후 요청: ~2-4초

**GPU 모드 (Apple Silicon):**
- 첫 요청: ~8-12초
- 이후 요청: ~4-6초

### 메모리 사용

- AI 모델: ~500MB - 2GB (모델에 따라)
- 이미지 처리: ~100-200MB/요청
- 권장 서버 메모리: 최소 4GB

---

## 참고 자료

- [FaceFusion GitHub](https://github.com/facefusion/facefusion)
- [FaceFusion 공식 문서](https://docs.facefusion.io)
- [프로젝트 pyproject.toml](../pyproject.toml) - 의존성 목록
- [백엔드 아키텍처 문서](./251121_0230-BACKEND_ARCHITECTURE.md)
