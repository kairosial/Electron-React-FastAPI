# ParticipationHistory 구현 완료 ✅

10일 데이터 보관 정책과 영구 통계 보관을 위한 ParticipationHistory 시스템이 완성되었습니다!

## 📊 개요

### 핵심 기능
1. **10일 자동 삭제** - 개인정보 보호를 위해 Participation 데이터를 10일 후 자동 삭제
2. **영구 통계 보관** - ParticipationHistory에 익명화된 통계 데이터 영구 보관
3. **실시간 추적** - QR 스캔, 다운로드, 인쇄 등 모든 사용자 활동 추적
4. **대시보드 지원** - 관리자용 대시보드를 위한 종합 통계 API 제공

---

## 🗄️ 데이터베이스 구조

### ParticipationHistory 테이블

```sql
CREATE TABLE participation_history (
    history_id INTEGER PRIMARY KEY,

    -- 원본 참조
    original_participation_id INTEGER NOT NULL,

    -- 분석용 메타데이터 (개인정보 제외)
    gender VARCHAR(10) NOT NULL,
    selected_profile_name VARCHAR(100),
    selected_talent_name VARCHAR(100),

    -- 오프라인 성과 (인쇄)
    is_printed_profile BOOLEAN DEFAULT FALSE,
    is_printed_talent BOOLEAN DEFAULT FALSE,

    -- 온라인 성과 (QR/다운로드)
    is_download_page_accessed BOOLEAN DEFAULT FALSE,
    download_count_profile INTEGER DEFAULT 0,
    download_count_talent INTEGER DEFAULT 0,

    -- 시간 정보
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 데이터 흐름

```
1. 사용자 체험 → Participation 생성
2. 체험 완료 → ParticipationHistory 생성 (익명 통계)
3. 인쇄/다운로드 → ParticipationHistory 업데이트
4. 10일 경과 → Participation 삭제 (개인정보)
5. 통계 조회 → ParticipationHistory 사용 (영구 보관)
```

---

## 🔄 자동 삭제 스케줄러

### 동작 방식

**파일**: [backend/scheduler.py](backend/scheduler.py:1)

- **서버 시작 시**: 즉시 1회 정리 실행
- **이후**: 24시간마다 자동 실행
- **삭제 기준**: `created_at < 현재시각 - 10일`
- **삭제 대상**: Participation 테이블만 (ParticipationHistory는 유지)

### 실행 로그 예시

```
2025-11-20 00:00:00 INFO 📅 일일 데이터 정리 작업 시작...
2025-11-20 00:00:01 INFO ✅ 15개의 10일 이상 된 참여 데이터가 삭제되었습니다. (기준일: 2025-11-10)
```

---

## 📡 새로운 API 엔드포인트

### 1. QR 스캔 추적

**POST** `/api/tracking/qr-scan`

사용자가 QR 코드를 스캔하여 다운로드 페이지에 접근할 때 호출합니다.

```json
// Request
{
  "uuid": "a3b5c7d9-1234-5678-90ab-cdef12345678"
}

// Response
{
  "success": true,
  "message": "QR 스캔이 기록되었습니다."
}
```

**프론트엔드 통합 예시:**
```javascript
// 다운로드 페이지 로드 시
async function onPageLoad(uuid) {
  await fetch('/api/tracking/qr-scan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ uuid })
  });
}
```

---

### 2. 다운로드 추적

**POST** `/api/tracking/download`

사용자가 이미지 다운로드 버튼을 클릭할 때 호출합니다.

```json
// Request
{
  "participation_id": 123,
  "image_type": "profile"  // 또는 "talent"
}

// Response
{
  "success": true,
  "message": "profile 다운로드가 기록되었습니다."
}
```

**프론트엔드 통합 예시:**
```javascript
// 다운로드 버튼 클릭 시
async function handleDownload(participationId, imageType) {
  // 다운로드 추적
  await fetch('/api/tracking/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      participation_id: participationId,
      image_type: imageType
    })
  });

  // 실제 다운로드 실행
  window.open(imageUrl, '_blank');
}
```

---

### 3. 대시보드 종합 통계

**GET** `/api/dashboard/statistics`

관리자 대시보드용 종합 통계를 조회합니다.

```bash
# 전체 기간 통계
curl http://localhost:8000/api/dashboard/statistics

# 특정 기간 통계
curl "http://localhost:8000/api/dashboard/statistics?start_date=2025-11-01&end_date=2025-11-20"
```

**응답 예시:**
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
      {"name": "영호", "count": 280},
      {"name": "순자", "count": 250}
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

---

### 4. 일별 통계

**GET** `/api/dashboard/daily-stats?days=7`

최근 N일간의 일별 통계를 조회합니다.

```bash
# 최근 7일
curl http://localhost:8000/api/dashboard/daily-stats?days=7

# 최근 30일
curl http://localhost:8000/api/dashboard/daily-stats?days=30
```

**응답 예시:**
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
    },
    // ... 7일치 데이터
  ]
}
```

---

## 🔗 데이터 연계 흐름

### 1. 체험 완료 시

```javascript
// 1. Participation 생성
const participation = await createParticipation({
  gender: 'male',
  original_image_path: 'uploads/user123.jpg',
  consent_agreed: true
});

// 2. ParticipationHistory 자동 생성 (백엔드에서)
// - original_participation_id: participation.id
// - gender: 'male'
// - 나머지 필드: 기본값
```

### 2. 인쇄 시

```javascript
// PrintLog 생성 + ParticipationHistory 업데이트
await fetch('/api/print', {
  method: 'POST',
  body: JSON.stringify({
    participation_id: 123,
    image_type: 'profile'
  })
});

// 백엔드에서 자동으로:
// - PrintLog 테이블에 기록 추가
// - ParticipationHistory.is_printed_profile = true로 업데이트
```

### 3. QR 스캔 시

```javascript
// 다운로드 페이지 로드
const uuid = new URLSearchParams(location.search).get('uuid');

// QR 스캔 추적
await fetch('/api/tracking/qr-scan', {
  method: 'POST',
  body: JSON.stringify({ uuid })
});

// 백엔드에서 자동으로:
// - UUID로 Participation 찾기
// - ParticipationHistory.is_download_page_accessed = true로 업데이트
```

### 4. 다운로드 시

```javascript
// 다운로드 버튼 클릭
await fetch('/api/tracking/download', {
  method: 'POST',
  body: JSON.stringify({
    participation_id: 123,
    image_type: 'profile'
  })
});

// 백엔드에서 자동으로:
// - ParticipationHistory.download_count_profile += 1
```

---

## 📈 대시보드 UI 구현 가이드

### 통계 카드 예시

```jsx
function DashboardStats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch('/api/dashboard/statistics')
      .then(res => res.json())
      .then(data => setStats(data.data));
  }, []);

  if (!stats) return <Loading />;

  return (
    <div className="stats-grid">
      <StatCard
        title="전체 체험자"
        value={stats.total_participations}
        icon="👥"
      />
      <StatCard
        title="QR 스캔율"
        value={`${stats.download_stats.qr_scan_rate}%`}
        icon="📱"
      />
      <StatCard
        title="인쇄율"
        value={`${stats.print_stats.print_rate}%`}
        icon="🖨️"
      />
      <StatCard
        title="평균 다운로드"
        value={stats.download_stats.avg_downloads_per_user}
        icon="⬇️"
      />
    </div>
  );
}
```

### 일별 차트 예시

```jsx
function DailyChart() {
  const [dailyData, setDailyData] = useState([]);

  useEffect(() => {
    fetch('/api/dashboard/daily-stats?days=7')
      .then(res => res.json())
      .then(data => setDailyData(data.data));
  }, []);

  return (
    <LineChart data={dailyData}>
      <Line dataKey="count" name="체험자" stroke="#8884d8" />
      <Line dataKey="prints" name="인쇄" stroke="#82ca9d" />
      <Line dataKey="downloads" name="다운로드" stroke="#ffc658" />
    </LineChart>
  );
}
```

---

## 🛠️ 유지보수

### 수동 데이터 정리

만약 즉시 데이터 정리가 필요하다면:

```python
# backend에서 직접 실행
from backend.scheduler import cleanup_old_participations
import asyncio

asyncio.run(cleanup_old_participations())
```

### 백업 및 복구

```bash
# 전체 데이터베이스 백업
cp data/kiosk.db data/backup_$(date +%Y%m%d).db

# ParticipationHistory만 추출 (CSV)
sqlite3 data/kiosk.db <<EOF
.headers on
.mode csv
.output history_export.csv
SELECT * FROM participation_history;
.quit
EOF
```

### 모니터링

```bash
# 현재 저장된 데이터 확인
sqlite3 data/kiosk.db "
SELECT
  COUNT(*) as total,
  COUNT(CASE WHEN created_at > datetime('now', '-10 days') THEN 1 END) as recent,
  COUNT(CASE WHEN created_at <= datetime('now', '-10 days') THEN 1 END) as old
FROM participation;
"

# ParticipationHistory 통계
sqlite3 data/kiosk.db "
SELECT
  COUNT(*) as total_history,
  SUM(CASE WHEN is_printed_profile OR is_printed_talent THEN 1 ELSE 0 END) as with_prints,
  SUM(CASE WHEN is_download_page_accessed THEN 1 ELSE 0 END) as qr_scanned
FROM participation_history;
"
```

---

## ✅ 구현 완료 체크리스트

- [x] ParticipationHistory 모델 생성
- [x] ParticipationHistory Repository 구현
- [x] Pydantic 스키마 정의
- [x] Alembic 마이그레이션 생성 및 실행
- [x] 10일 자동 삭제 스케줄러 구현
- [x] FastAPI에 스케줄러 통합
- [x] QR 스캔 추적 API
- [x] 다운로드 추적 API
- [x] 대시보드 종합 통계 API
- [x] 일별 통계 API

---

## 📝 다음 단계

1. **프론트엔드 통합**
   - 다운로드 페이지에 QR 스캔 추적 코드 추가
   - 다운로드 버튼에 추적 코드 추가
   - 관리자 대시보드 UI 개발

2. **테스트**
   - 전체 워크플로우 테스트
   - 10일 자동 삭제 동작 검증
   - 통계 정확성 확인

3. **모니터링**
   - 스케줄러 로그 확인
   - 데이터베이스 용량 모니터링
   - API 성능 모니터링

---

**작성일**: 2025-11-20
**상태**: ✅ 완전히 구현 완료
