# 데이터베이스 구현 완료 ✅

SQLite 기반 데이터베이스가 성공적으로 구현되었습니다!

## 📊 구현된 내용

### 1. 데이터베이스 구조 (ERD 기반)

4개의 테이블이 생성되었습니다:

#### **Participation** (참여 세션)
- `participation_id` (PK)
- `consent_agreed` (동의 여부)
- `gender` (성별)
- `original_image_path` (원본 이미지 경로)
- `selected_profile_id` (FK → TargetProfile)
- `selected_talent_id` (FK → TargetTalent)
- `generated_profile_image_path` (생성된 프로필 이미지)
- `generated_talent_image_path` (생성된 장기자랑 이미지)
- `download_page_uuid` (다운로드 UUID, unique)
- `created_at` (생성 시각)

#### **TargetProfile** (프로필 타겟)
- `profile_id` (PK)
- `profile_name` (프로필 이름, unique)
- `gender_filter` (male/female)
- `target_image_path` (타겟 이미지 경로)

#### **TargetTalent** (장기자랑 타겟)
- `talent_id` (PK)
- `talent_name` (장기자랑 이름, unique)
- `gender_filter` (male/female)
- `target_image_path` (타겟 이미지 경로)

#### **PrintLog** (인쇄 기록)
- `print_log_id` (PK)
- `participation_id` (FK → Participation)
- `image_type` (profile/talent)
- `printed_at` (인쇄 시각)

---

### 2. 파일 구조

```
backend/
├── database.py                  # ✅ DB 연결 관리
├── models/                      # ✅ SQLAlchemy 모델
│   ├── __init__.py
│   ├── participation.py
│   ├── target_profile.py
│   ├── target_talent.py
│   └── print_log.py
├── repositories/                # ✅ 데이터 접근 계층
│   ├── __init__.py
│   ├── base.py
│   ├── participation_repo.py
│   ├── profile_repo.py
│   ├── talent_repo.py
│   └── print_log_repo.py
├── schemas/                     # ✅ Pydantic 스키마
│   ├── __init__.py
│   ├── participation.py
│   ├── target.py
│   └── print_log.py
├── migrations/                  # ✅ Alembic 마이그레이션
│   ├── env.py
│   ├── versions/
│   │   └── f823a5a0fa14_initial_database_schema.py
│   └── README
├── scripts/                     # ✅ 유틸리티 스크립트
│   └── seed_data.py
├── alembic.ini                  # ✅ Alembic 설정
├── main.py                      # ✅ FastAPI (DB 통합)
└── .env                         # ✅ 환경 변수

data/
└── kiosk.db                     # ✅ SQLite 데이터베이스 파일
```

---

### 3. 초기 데이터 (Seed Data)

#### 프로필 타겟 (4개)
1. 광수 (male)
2. 영호 (male)
3. 순자 (female)
4. 영숙 (female)

#### 장기자랑 타겟 (5개)
1. 기타 연주 (male)
2. 춤 (남자) (male)
3. 노래 (남자) (male)
4. 춤 (여자) (female)
5. 노래 (여자) (female)

---

### 4. 새로운 API 엔드포인트

#### **프로필/장기자랑 조회**
- `GET /api/profiles` - 프로필 목록 조회
- `GET /api/profiles?gender=male` - 성별로 필터링
- `GET /api/talents` - 장기자랑 목록 조회
- `GET /api/talents?gender=female` - 성별로 필터링

#### **세션 관리**
- `POST /api/session/start` - 새 세션 시작
  ```json
  {
    "gender": "male",
    "original_image_path": "path/to/image.jpg",
    "consent_agreed": true
  }
  ```
- `GET /api/session/{uuid}` - UUID로 세션 조회

#### **인쇄 기록**
- `POST /api/print` - 인쇄 기록 생성
  ```json
  {
    "participation_id": 1,
    "image_type": "profile"
  }
  ```

#### **통계**
- `GET /api/statistics` - 전체 통계 조회

#### **기존 API (유지)**
- `POST /api/generate/profile` - 프로필 이미지 생성
- `POST /api/generate/talent` - 장기자랑 이미지 생성

---

## 🚀 서버 실행 방법

### 1. 환경 확인

```bash
# 데이터베이스 파일 확인
ls -la data/kiosk.db

# 환경 변수 확인
cat backend/.env | grep DATABASE_URL
```

### 2. 서버 시작

```bash
cd backend
poetry run python main.py
```

또는 start.sh 사용:

```bash
./backend/start.sh
```

### 3. API 문서 확인

서버 시작 후 브라우저에서:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 테스트 방법

### 1. 프로필 목록 조회

```bash
curl http://localhost:8000/api/profiles
```

예상 응답:
```json
[
  {
    "profile_id": 1,
    "profile_name": "광수",
    "gender_filter": "male",
    "target_image_path": "assets/profile_targets/kwangsu.jpg"
  },
  ...
]
```

### 2. 세션 시작

```bash
curl -X POST http://localhost:8000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "male",
    "original_image_path": "uploads/test.jpg",
    "consent_agreed": true
  }'
```

### 3. 통계 조회

```bash
curl http://localhost:8000/api/statistics
```

---

## 📝 데이터베이스 관리

### 마이그레이션 생성

```bash
cd backend
poetry run alembic revision --autogenerate -m "설명"
```

### 마이그레이션 적용

```bash
poetry run alembic upgrade head
```

### 마이그레이션 롤백

```bash
poetry run alembic downgrade -1
```

### 초기 데이터 재입력

```bash
poetry run python scripts/seed_data.py
```

---

## 🔧 환경 변수

`backend/.env` 파일:

```env
# 데이터베이스 URL
DATABASE_URL=sqlite+aiosqlite:////Users/syk/PC/git/Electron-React-FastAPI/data/kiosk.db

# FaceFusion 설정 (기존)
FACEFUSION_MODE=cpu
...
```

---

## ✅ 구현 완료 체크리스트

- [x] SQLite 데이터베이스 설정
- [x] SQLAlchemy 비동기 모델 (4개 테이블)
- [x] Repository 패턴 구현
- [x] Pydantic 스키마 정의
- [x] Alembic 마이그레이션 설정
- [x] 초기 데이터 Seed 스크립트
- [x] FastAPI API 엔드포인트 통합
- [x] 데이터베이스 초기화 자동화

---

## 🎯 다음 단계

1. **프론트엔드 통합**
   - React에서 새로운 API 엔드포인트 호출
   - 세션 관리 로직 추가
   - 프로필/장기자랑 선택 UI 구현

2. **기능 확장**
   - 이미지 생성 시 DB에 자동 기록
   - UUID 기반 다운로드 페이지
   - QR 코드 생성 (UUID 링크)

3. **운영 최적화**
   - 정기 백업 스크립트
   - 로그 로테이션
   - 오래된 세션 정리

---

## 📚 참고

- **SQLAlchemy 문서**: https://docs.sqlalchemy.org/
- **Alembic 문서**: https://alembic.sqlalchemy.org/
- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **Pydantic 문서**: https://docs.pydantic.dev/

---

**작성일**: 2025-11-18
**상태**: ✅ 구현 완료
