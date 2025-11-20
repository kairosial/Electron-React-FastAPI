# API Endpoints (v1)

모든 API 엔드포인트는 `/api/v1/` prefix를 사용합니다.

## 📋 목차

- [기본 엔드포인트](#기본-엔드포인트)
- [세션 관리](#세션-관리)
- [프로필/장기자랑](#프로필장기자랑)
- [이미지 생성](#이미지-생성)
- [인쇄 관리](#인쇄-관리)
- [추적 (Tracking)](#추적-tracking)
- [대시보드/통계](#대시보드통계)

---

## 기본 엔드포인트

### GET `/`
서버 상태 확인

**Response:**
```json
{
  "message": "나는솔로 키오스크 백엔드 서버",
  "status": "running",
  "mode": "mock_facefusion"
}
```

### GET `/health`
헬스 체크

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 세션 관리

### POST `/api/v1/session/start`
새로운 참여 세션 시작

**Request Body:**
```json
{
  "gender": "male",
  "original_image_path": "uploads/user123.jpg",
  "consent_agreed": true
}
```

**Response:**
```json
{
  "participation_id": 123,
  "consent_agreed": true,
  "gender": "male",
  "original_image_path": "uploads/user123.jpg",
  "download_page_uuid": "a3b5c7d9-1234-5678-90ab-cdef12345678",
  "created_at": "2025-11-20T12:00:00"
}
```

### GET `/api/v1/session/{uuid}`
UUID로 세션 조회 (다운로드 페이지용)

**Parameters:**
- `uuid`: 다운로드 페이지 UUID

**Response:**
```json
{
  "participation_id": 123,
  "gender": "male",
  "generated_profile_image_path": "output/profile_123.jpg",
  "generated_talent_image_path": "output/talent_123.jpg",
  "download_page_uuid": "a3b5c7d9-1234-5678-90ab-cdef12345678",
  "created_at": "2025-11-20T12:00:00"
}
```

---

## 프로필/장기자랑

### GET `/api/v1/profiles`
사용 가능한 프로필 목록 조회

**Query Parameters:**
- `gender` (optional): `male` 또는 `female`

**Response:**
```json
[
  {
    "profile_id": 1,
    "profile_name": "광수",
    "gender_filter": "male",
    "target_image_path": "assets/profile_targets/kwangsu.jpg"
  },
  {
    "profile_id": 2,
    "profile_name": "영호",
    "gender_filter": "male",
    "target_image_path": "assets/profile_targets/youngho.jpg"
  }
]
```

### GET `/api/v1/talents`
사용 가능한 장기자랑 목록 조회

**Query Parameters:**
- `gender` (optional): `male` 또는 `female`

**Response:**
```json
[
  {
    "talent_id": 1,
    "talent_name": "기타 연주",
    "gender_filter": "male",
    "target_image_path": "assets/talent_targets/guitar_male.jpg"
  },
  {
    "talent_id": 4,
    "talent_name": "춤 (여자)",
    "gender_filter": "female",
    "target_image_path": "assets/talent_targets/dance_female.jpg"
  }
]
```

---

## 이미지 생성

### POST `/api/v1/generate/profile`
프로필 이미지 생성 (FaceFusion)

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (이미지 파일)

**Response:**
```json
{
  "success": true,
  "image_url": "http://localhost:8000/images/profile_20251120_120530_abc123.jpg",
  "filename": "profile_20251120_120530_abc123.jpg",
  "message": "프로필 이미지가 성공적으로 생성되었습니다."
}
```

### POST `/api/v1/generate/talent`
장기자랑 이미지 생성 (FaceFusion)

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (이미지 파일)

**Response:**
```json
{
  "success": true,
  "image_url": "http://localhost:8000/images/talent_20251120_120530_abc123.jpg",
  "filename": "talent_20251120_120530_abc123.jpg",
  "message": "탤런트쇼 이미지가 성공적으로 생성되었습니다."
}
```

---

## 인쇄 관리

### POST `/api/v1/print`
인쇄 기록 생성

**Request Body:**
```json
{
  "participation_id": 123,
  "image_type": "profile"  // 또는 "talent"
}
```

**Response:**
```json
{
  "print_log_id": 456,
  "participation_id": 123,
  "image_type": "profile",
  "printed_at": "2025-11-20T12:00:00"
}
```

---

## 추적 (Tracking)

### POST `/api/v1/tracking/qr-scan`
QR 코드 스캔 추적

**Request Body:**
```json
{
  "uuid": "a3b5c7d9-1234-5678-90ab-cdef12345678"
}
```

**Response:**
```json
{
  "success": true,
  "message": "QR 스캔이 기록되었습니다."
}
```

**사용 예시 (프론트엔드):**
```javascript
// 다운로드 페이지 로드 시
const uuid = new URLSearchParams(location.search).get('uuid');
await fetch('/api/v1/tracking/qr-scan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ uuid })
});
```

### POST `/api/v1/tracking/download`
다운로드 버튼 클릭 추적

**Request Body:**
```json
{
  "participation_id": 123,
  "image_type": "profile"  // 또는 "talent"
}
```

**Response:**
```json
{
  "success": true,
  "message": "profile 다운로드가 기록되었습니다."
}
```

**사용 예시 (프론트엔드):**
```javascript
// 다운로드 버튼 클릭 시
async function handleDownload(participationId, imageType) {
  // 추적
  await fetch('/api/v1/tracking/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      participation_id: participationId,
      image_type: imageType
    })
  });

  // 다운로드
  window.open(imageUrl, '_blank');
}
```

---

## 대시보드/통계

### GET `/api/v1/statistics`
전체 통계 조회 (기존 호환성 유지)

**Response:**
```json
{
  "print_statistics": {
    "profile": 450,
    "talent": 380,
    "total": 830
  },
  "recent_sessions_count": 5
}
```

### GET `/api/v1/dashboard/statistics`
대시보드용 종합 통계 (ParticipationHistory 기반)

**Query Parameters:**
- `start_date` (optional): 시작 날짜 (YYYY-MM-DD)
- `end_date` (optional): 종료 날짜 (YYYY-MM-DD)

**Example:**
```bash
# 전체 통계
GET /api/v1/dashboard/statistics

# 특정 기간 통계
GET /api/v1/dashboard/statistics?start_date=2025-11-01&end_date=2025-11-20
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_participations": 1250,
    "gender_stats": {
      "male": 680,
      "female": 570
    },
    "print_stats": {
      "profile_printed": 450,
      "talent_printed": 380,
      "total_prints": 830,
      "print_rate": 33.2
    },
    "download_stats": {
      "qr_scanned": 890,
      "qr_scan_rate": 71.2,
      "total_downloads_profile": 1150,
      "total_downloads_talent": 980,
      "avg_downloads_per_user": 1.70
    },
    "popular_profiles": [
      {"name": "광수", "count": 320},
      {"name": "영호", "count": 280}
    ],
    "popular_talents": [
      {"name": "기타 연주", "count": 400},
      {"name": "춤 (여자)", "count": 350}
    ]
  },
  "period": {
    "start": "2025-11-01",
    "end": "2025-11-20"
  }
}
```

### GET `/api/v1/dashboard/daily-stats`
일별 통계 조회

**Query Parameters:**
- `days` (default: 7): 조회할 일수 (1-365)

**Example:**
```bash
# 최근 7일
GET /api/v1/dashboard/daily-stats?days=7

# 최근 30일
GET /api/v1/dashboard/daily-stats?days=30
```

**Response:**
```json
{
  "success": true,
  "days": 7,
  "data": [
    {
      "date": "2025-11-14",
      "count": 85,
      "prints": 28,
      "downloads": 142
    },
    {
      "date": "2025-11-15",
      "count": 92,
      "prints": 31,
      "downloads": 156
    }
  ]
}
```

---

## API 테스트

### Swagger UI
http://localhost:8000/docs

### ReDoc
http://localhost:8000/redoc

### cURL 예시

```bash
# 프로필 목록 조회
curl http://localhost:8000/api/v1/profiles

# 남성 프로필만 조회
curl http://localhost:8000/api/v1/profiles?gender=male

# 세션 시작
curl -X POST http://localhost:8000/api/v1/session/start \
  -H "Content-Type: application/json" \
  -d '{"gender":"male","original_image_path":"uploads/test.jpg","consent_agreed":true}'

# QR 스캔 추적
curl -X POST http://localhost:8000/api/v1/tracking/qr-scan \
  -H "Content-Type: application/json" \
  -d '{"uuid":"a3b5c7d9-1234-5678-90ab-cdef12345678"}'

# 대시보드 통계
curl http://localhost:8000/api/v1/dashboard/statistics

# 최근 7일 통계
curl http://localhost:8000/api/v1/dashboard/daily-stats?days=7
```

---

## 버전 관리

### 현재 버전: v1

모든 API는 `/api/v1/` prefix를 사용합니다. 향후 Breaking Change가 필요한 경우 `/api/v2/`를 추가할 수 있습니다.

### 마이그레이션 가이드

기존 `/api/` 경로를 사용하던 코드는 `/api/v1/`로 업데이트해야 합니다:

```javascript
// Before
fetch('/api/profiles')

// After
fetch('/api/v1/profiles')
```

---

**작성일**: 2025-11-20
**API 버전**: v1
**서버**: FastAPI 0.115.0
