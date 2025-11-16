# FaceFusion 환경 설정 완료

## 설정 완료 항목

### ✅ 1. Poetry 의존성 설정
**파일:** `pyproject.toml`

FaceFusion 실행에 필요한 모든 의존성이 추가되었습니다:
- `numpy` (>=2.0.0,<2.3.0)
- `onnx` (^1.19.1)
- `onnxruntime` (^1.23.2)
- `opencv-python` (^4.12.0)
- `psutil` (^7.1.2)
- `tqdm` (^4.67.1)
- `scipy` (^1.13.0)
- `gradio` (^5.44.1)
- `gradio-rangeslider` (^0.0.8)

**설치 명령:**
```bash
poetry install
```

---

### ✅ 2. 환경 변수 설정
**파일:** `backend/.env`

FaceFusion 설정을 위한 환경 변수 파일이 생성되었습니다:
- `FACEFUSION_MODE`: CPU/GPU 모드 설정
- `FACEFUSION_EXECUTION_PROVIDERS`: 실행 프로바이더
- `FACEFUSION_MODEL_PATH`: AI 모델 저장 경로
- `PROFILE_TARGETS_DIR`: 프로필 타겟 이미지 경로
- `TALENT_TARGETS_DIR`: 재능 타겟 이미지 경로
- `MAX_PROCESSING_TIME`: 처리 타임아웃
- `FACE_ENHANCER`: 얼굴 향상 모델
- `FACE_DETECTOR`: 얼굴 감지 모델
- `FACEFUSION_PATH`: FaceFusion 라이브러리 경로

---

### ✅ 3. 시작 스크립트 업데이트
**파일:** `backend/start.sh`

다음 기능이 추가되었습니다:
- **상대 경로 자동 감지**: FaceFusion을 `../facefusion`에서 자동으로 찾음
- **환경 변수 지원**: `.env`에서 `FACEFUSION_PATH` 설정 가능
- **경로 검증**: FaceFusion이 올바르게 설치되었는지 자동 확인
- `.env` 파일 자동 로드
- Poetry 환경에서 서버 실행

**실행 방법:**
```bash
cd backend
chmod +x start.sh
./start.sh
```

**작동 방식:**
1. `.env` 파일에서 `FACEFUSION_PATH` 확인
2. 설정되지 않았으면 `../facefusion` 경로에서 자동 탐색
3. `facefusion/__init__.py` 파일 존재 여부로 검증
4. 찾지 못하면 명확한 에러 메시지 출력

---

### ✅ 4. 디렉토리 구조 생성

프로젝트에 다음 디렉토리가 생성되었습니다:

```
Electron-React-FastAPI/
├── assets/
│   ├── profile_targets/     # 프로필용 타겟 이미지 저장
│   └── talent_targets/      # 재능쇼용 타겟 이미지 저장
├── models/                  # FaceFusion AI 모델 저장
└── output/                  # 생성된 이미지 저장 (기존)
```

---

### ✅ 5. FaceFusion Import 검증

FaceFusion이 정상적으로 임포트되는지 확인되었습니다:

```python
import sys
sys.path.insert(0, '/Users/syk/PC/git/facefusion')
import facefusion
# ✅ 성공!
```

---

## 다음 단계

### 1. 타겟 이미지 준비 (필수)

얼굴 합성에 사용할 타겟 이미지를 준비해야 합니다:

```bash
# 프로필용 이미지 (5-10장)
# 파일 위치: assets/profile_targets/
# 예: profile_1.jpg, profile_2.jpg, ...

# 재능쇼용 이미지 (5-10장)
# 파일 위치: assets/talent_targets/
# 예: talent_1.jpg, talent_2.jpg, ...
```

**이미지 요구사항:**
- 형식: JPG, PNG
- 최소 해상도: 512x512 (권장)
- 얼굴이 명확하게 보이는 정면 사진
- 한 이미지당 한 명의 얼굴만

---

### 2. FaceFusion 모델 다운로드 (선택)

FaceFusion은 첫 실행 시 필요한 모델을 자동으로 다운로드합니다.
수동으로 다운로드하려면:

```bash
cd /Users/syk/PC/git/facefusion
python facefusion.py --help
```

주요 모델:
- `inswapper_128.onnx` - 얼굴 합성 모델
- RetinaFace/YuNet - 얼굴 감지 모델
- GFPGAN/CodeFormer - 얼굴 향상 모델

---

### 3. Backend 서비스 구현

현재 `backend/facefusion_service.py`는 Mock 구현입니다.
다음 작업이 필요합니다:

1. **Import FaceFusion 모듈**
   ```python
   import sys
   sys.path.insert(0, '/Users/syk/PC/git/facefusion')
   from facefusion import core
   ```

2. **실제 얼굴 합성 구현**
   - `generate_profile_image()` 함수 업데이트
   - `generate_talent_image()` 함수 업데이트

3. **타겟 이미지 랜덤 선택 로직 추가**

4. **에러 핸들링 강화**
   - 얼굴 미감지
   - 여러 얼굴 감지
   - 처리 타임아웃

---

## 테스트

### 환경 설정 테스트

```bash
# FaceFusion import 테스트
cd /Users/syk/PC/git/Electron-React-FastAPI
export PYTHONPATH="/Users/syk/PC/git/facefusion:$PYTHONPATH"
poetry run python -c "import facefusion; print('✅ Success!')"
```

### 서버 실행 테스트

```bash
cd backend
./start.sh
```

예상 출력:
```
======================================
나는솔로 키오스크 백엔드 서버 시작
======================================

Python 버전 확인 중...
Python 3.11.x

✅ FaceFusion 통합 모드로 실행됩니다
실제 AI 얼굴 합성이 수행됩니다.

FaceFusion 경로 설정: /Users/syk/PC/git/facefusion
.env 파일 로드됨
서버 시작 중... (http://localhost:8000)

INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## GPU 설정 (선택)

GPU를 사용하려면 (NVIDIA GPU가 있는 경우):

1. **CUDA 설치** (필요 시)
   - CUDA Toolkit 설치
   - cuDNN 설치

2. **onnxruntime-gpu 설치**
   ```bash
   poetry remove onnxruntime
   poetry add onnxruntime-gpu
   ```

3. **환경 변수 수정**
   ```bash
   # backend/.env
   FACEFUSION_MODE=gpu
   FACEFUSION_EXECUTION_PROVIDERS=CUDAExecutionProvider,CPUExecutionProvider
   ```

---

## 트러블슈팅

### Import Error 발생 시

```bash
export PYTHONPATH="/Users/syk/PC/git/facefusion:$PYTHONPATH"
```

### 의존성 충돌 발생 시

```bash
poetry lock --no-update
poetry install
```

### 모델 다운로드 실패 시

FaceFusion 디렉토리에서 수동 다운로드:
```bash
cd /Users/syk/PC/git/facefusion
python install.py
```

---

## 요약

✅ **완료된 작업:**
1. Poetry 의존성 설정 및 설치
2. 환경 변수 파일 생성
3. 시작 스크립트 업데이트
4. 디렉토리 구조 생성
5. FaceFusion import 검증

⏭️ **다음 작업:**
1. 타겟 이미지 준비
2. Backend 서비스 실제 구현
3. API 에러 핸들링 강화
4. 성능 최적화
5. 전체 테스트

현재 환경 설정은 완료되었으며, 이제 실제 FaceFusion 로직을 구현할 준비가 되었습니다!
