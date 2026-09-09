# 🔧 Backend — Complete Task List

> **Scope**: Only the `backend/` directory  
> **Current Status**: Core API working · Missing history endpoints, auth, hardening, and production readiness

---

## 📁 Current Backend File Structure

```
backend/
├── Dockerfile              ✅ Basic, needs hardening
├── requirements.txt        ⚠️ Missing pinned versions & dev deps
├── config.py               ⚠️ No validation, no pydantic-settings
├── main.py                 ⚠️ All routes + schemas in single file
├── database/
│   ├── __init__.py          ✅ 
│   └── db.py                ⚠️ Only write (log_prediction), no read/query functions
└── services/
    ├── __init__.py          ✅ 
    └── ml_client.py         ⚠️ Creates new httpx client per request (no pooling)
```

---

## ✅ What's Already Done

| # | Item | File | Notes |
|---|------|------|-------|
| 1 | FastAPI app setup with lifespan | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L80-L92) | Initializes DB on startup, closes on shutdown |
| 2 | `POST /api/v1/fertilizer/recommend` | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L102-L170) | Full flow: validate → call ML → persist → respond |
| 3 | `GET /api/v1/health` | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L172-L178) | Checks backend + ML service health |
| 4 | `GET /api/v1/ready` | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L180-L186) | Checks backend + ML service readiness |
| 5 | Pydantic request validation | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L45-L68) | pH range, non-negative values, finite check |
| 6 | Pydantic response model | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L70-L78) | Includes fertilizer, confidence, versions, probabilities |
| 7 | Async ML HTTP client | [ml_client.py](file:///e:/Fertilizer_Recommend/backend/services/ml_client.py#L19-L91) | Handles timeout, connect, HTTP, and validation errors |
| 8 | ML health & ready checks | [ml_client.py](file:///e:/Fertilizer_Recommend/backend/services/ml_client.py#L93-L111) | Non-throwing, returns status dict |
| 9 | SQLite/PostgreSQL database | [db.py](file:///e:/Fertilizer_Recommend/backend/database/db.py#L22-L34) | Auto-detects from `DATABASE_URL` |
| 10 | PredictionLog ORM model | [db.py](file:///e:/Fertilizer_Recommend/backend/database/db.py#L46-L78) | Full version tracking, input/output, timestamps |
| 11 | `log_prediction()` function | [db.py](file:///e:/Fertilizer_Recommend/backend/database/db.py#L98-L142) | Non-crashing (catches DB errors gracefully) |
| 12 | CORS middleware | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L94-L100) | `allow_origins=["*"]` (wide open — needs restriction) |
| 13 | Global exception handler | [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L188-L194) | Catches unhandled exceptions, returns 500 |
| 14 | Dockerfile | [Dockerfile](file:///e:/Fertilizer_Recommend/backend/Dockerfile) | Python 3.13-slim, uvicorn |

---

## ❌ What Needs to Be Done

### 🔴 Must-Have (Complete the backend properly)

#### 1. Prediction History — Read Endpoints
> **Currently**: Database has `log_prediction()` (write-only). There is **no way to query past predictions**.

**Files to modify**: [db.py](file:///e:/Fertilizer_Recommend/backend/database/db.py), [main.py](file:///e:/Fertilizer_Recommend/backend/main.py)

```
New endpoints needed:
  GET  /api/v1/predictions              → List predictions (paginated)
  GET  /api/v1/predictions/{id}         → Get single prediction by ID
  GET  /api/v1/predictions/stats        → Aggregated statistics
```

**DB functions to add in `db.py`:**
- [ ] `get_prediction(prediction_id: str) → PredictionLog | None`
- [ ] `list_predictions(page, per_page, filters) → list[PredictionLog]`
- [ ] `count_predictions(filters) → int`
- [ ] `get_prediction_stats() → dict` (most frequent fertilizer, avg confidence, total count, daily counts)

---

#### 2. Request Latency Tracking
> **Currently**: `PredictionLog.latency_ms` column exists but is **never populated** — `latency_ms` is never measured or passed.

**File to modify**: [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L102-L170)

- [ ] Add `time.perf_counter()` before/after ML call
- [ ] Pass `latency_ms` to `log_prediction()`
- [ ] Include `latency_ms` in the API response

---

#### 3. Separate Schemas into Own Module
> **Currently**: `RecommendRequest` and `RecommendResponse` are defined inside [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L44-L78) — mixing routing with data models.

**New file**: `backend/schemas/`
- [ ] Create `backend/schemas/__init__.py`
- [ ] Create `backend/schemas/recommendation.py` — move `RecommendRequest`, `RecommendResponse`
- [ ] Create `backend/schemas/prediction.py` — add `PredictionDetail`, `PredictionListResponse`, `PredictionStatsResponse`
- [ ] Create `backend/schemas/common.py` — add `PaginatedResponse`, `ErrorResponse`

---

#### 4. CORS Origin Restriction
> **Currently**: `allow_origins=["*"]` at [main.py L95](file:///e:/Fertilizer_Recommend/backend/main.py#L95) — allows any domain. This is a security risk.

**File to modify**: [config.py](file:///e:/Fertilizer_Recommend/backend/config.py), [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L94-L100)

- [ ] Add `ALLOWED_ORIGINS` to settings (comma-separated env var)
- [ ] Default to `["http://localhost:3000", "http://localhost:5173"]` for dev
- [ ] Use env-based list in CORS middleware

---

#### 5. Crop_Growth_Stage Enum Validation
> **Currently**: `Crop_Growth_Stage` is `str` with no validation — any string is accepted. The model only recognizes: `Sowing`, `Vegetative`, `Flowering`, `Harvest`.

**File to modify**: [main.py](file:///e:/Fertilizer_Recommend/backend/main.py#L51) (or new schemas file)

- [ ] Create `CropGrowthStage` enum: `Sowing | Vegetative | Flowering | Harvest`
- [ ] Use it as the type for `Crop_Growth_Stage` field
- [ ] Return 422 with clear error for invalid values

---

#### 6. Structured JSON Logging
> **Currently**: Plain text logging at [main.py L21-L26](file:///e:/Fertilizer_Recommend/backend/main.py#L21-L26) — not parseable by log aggregation tools.

**New file**: `backend/logging_config.py`

- [ ] JSON log formatter with fields: `timestamp`, `level`, `logger`, `message`, `request_id`, `extra`
- [ ] Correlation ID propagation across request lifecycle
- [ ] Separate log levels for dev (pretty print) vs prod (JSON)

---

#### 7. HTTP Connection Pooling (MLClient)
> **Currently**: [ml_client.py L42](file:///e:/Fertilizer_Recommend/backend/services/ml_client.py#L42) creates a **new `httpx.AsyncClient` per request** — wasteful, no connection reuse.

**File to modify**: [ml_client.py](file:///e:/Fertilizer_Recommend/backend/services/ml_client.py)

- [ ] Create a persistent `httpx.AsyncClient` in `__init__` or via app lifespan
- [ ] Add `async close()` method
- [ ] Call `ml_client.close()` in app shutdown (lifespan)

---

#### 8. Dockerfile Hardening
> **Currently**: [Dockerfile](file:///e:/Fertilizer_Recommend/backend/Dockerfile) runs as root, no `.dockerignore`, no health check.

**File to modify**: `backend/Dockerfile`, **New file**: `backend/.dockerignore`

- [ ] Add non-root user (`RUN useradd appuser && USER appuser`)
- [ ] Create `.dockerignore` (exclude `__pycache__`, `.git`, tests, etc.)
- [ ] Add `HEALTHCHECK` instruction
- [ ] Pin Python version (`python:3.13.1-slim` not just `3.13-slim`)
- [ ] Add `--no-root` to pip install

---

#### 9. API Route Modularization (Routers)
> **Currently**: All 3 endpoints are in a single [main.py](file:///e:/Fertilizer_Recommend/backend/main.py). As endpoints grow, this will become unmanageable.

**New files**: `backend/routers/`
- [ ] `backend/routers/__init__.py`
- [ ] `backend/routers/recommendation.py` — `POST /recommend`
- [ ] `backend/routers/predictions.py` — `GET /predictions`, `GET /predictions/{id}`, `GET /predictions/stats`
- [ ] `backend/routers/system.py` — `GET /health`, `GET /ready`
- [ ] Slim down `main.py` to app creation + router includes only

---

#### 10. Config Validation
> **Currently**: [config.py](file:///e:/Fertilizer_Recommend/backend/config.py) uses raw `os.environ.get()` — no type validation, no error on missing critical vars.

**File to modify**: [config.py](file:///e:/Fertilizer_Recommend/backend/config.py)

- [ ] Switch to `pydantic-settings` (`BaseSettings` with `.env` support)
- [ ] Add validators (e.g., `ML_SERVICE_URL` must be valid URL, `ML_REQUEST_TIMEOUT` must be > 0)
- [ ] Fail fast on startup if required config is missing/invalid
- [ ] Add `pydantic-settings` to `requirements.txt`

---

### 🟡 Should-Have (Production readiness)

#### 11. Authentication & API Key Management
- [ ] Create `backend/middleware/auth.py`
- [ ] Add API key validation middleware (`X-API-Key` header)
- [ ] Store API keys in env var or database
- [ ] Add `api_key` to settings
- [ ] Make `/health` public but `/recommend` and `/predictions` protected

#### 12. Rate Limiting
- [ ] Add `slowapi` or custom middleware for rate limiting
- [ ] Configure per-IP and per-API-key limits
- [ ] Return `429 Too Many Requests` with `Retry-After` header
- [ ] Add `slowapi` to `requirements.txt`

#### 13. Pagination Helper
- [ ] Create a reusable pagination utility (`backend/utils/pagination.py`)
- [ ] Standard query params: `page`, `per_page`, `sort_by`, `order`
- [ ] Response format: `{ items: [], total: N, page: N, per_page: N, total_pages: N }`

#### 14. Analytics / Dashboard Endpoint
- [ ] `GET /api/v1/analytics/summary` — total predictions, success/error rate, avg confidence
- [ ] `GET /api/v1/analytics/distribution` — prediction count per fertilizer type
- [ ] `GET /api/v1/analytics/timeline` — predictions over time (daily/weekly)
- [ ] `GET /api/v1/analytics/model-performance` — avg confidence per model version

#### 15. ML Client Retry Logic
- [ ] Add configurable retry with exponential backoff for transient ML service failures
- [ ] Retry on `503`, `504`, `ConnectError` — not on `400`, `422`
- [ ] Max retries configurable via env var
- [ ] Add `tenacity` to `requirements.txt` or implement manually

#### 16. Circuit Breaker Pattern
- [ ] Track ML service failure rate over sliding window
- [ ] Trip circuit (stop calling ML) after N consecutive failures
- [ ] Return cached/fallback response or graceful 503 when circuit is open
- [ ] Auto-reset circuit after cooldown period

#### 17. Database Migrations
- [ ] Add `peewee-migrate` or custom migration scripts
- [ ] Create initial migration from current schema
- [ ] Run migrations on app startup (after `init_db`)
- [ ] Track migration history in DB

#### 18. Request ID Middleware
- [ ] Create middleware that generates/extracts `X-Request-ID` from incoming requests
- [ ] Pass `request_id` through entire request lifecycle
- [ ] Include `request_id` in all log lines
- [ ] Return `X-Request-ID` in response headers

#### 19. Comprehensive Unit Tests
- [ ] Test each DB function individually (`get_prediction`, `list_predictions`, pagination)
- [ ] Test all error paths in `ml_client.py` (retry, circuit breaker)
- [ ] Test input validation edge cases (boundary values, invalid enums)
- [ ] Test auth middleware (valid/invalid/missing API keys)
- [ ] Add `pytest-cov` and achieve ≥80% coverage

#### 20. OpenAPI Documentation Enhancement
- [ ] Add detailed descriptions to all endpoints
- [ ] Add request/response examples
- [ ] Add error response schemas (`4xx`, `5xx`)
- [ ] Add tags for endpoint grouping
- [ ] Add API version info and contact details in FastAPI metadata

---

### 🟢 Nice-to-Have (Enhancements)

#### 21. Batch Prediction Endpoint
- [ ] `POST /api/v1/fertilizer/recommend/batch` — accepts array of inputs
- [ ] Concurrent ML calls with `asyncio.gather()`
- [ ] Response: array of results with per-item status
- [ ] Max batch size limit (configurable)

#### 22. User Feedback Endpoint
- [ ] `POST /api/v1/predictions/{id}/feedback` — submit correct/incorrect + actual fertilizer
- [ ] New `FeedbackLog` DB model
- [ ] Link feedback to prediction via `prediction_id`

#### 23. WebSocket for Real-time Updates
- [ ] `WS /api/v1/ws/predictions` — stream new predictions in real-time
- [ ] Useful for dashboard/monitoring frontend

#### 24. Response Caching (Redis)
- [ ] Cache ML predictions by input hash
- [ ] TTL-based expiration (e.g., 1 hour)
- [ ] Cache hit/miss logging
- [ ] Add `redis` and `aioredis` to requirements

#### 25. Background Task Processing
- [ ] Move DB logging to FastAPI `BackgroundTasks`
- [ ] Non-blocking prediction persistence (reduce response time)
- [ ] Error queue for failed DB writes

#### 26. Data Export Endpoint
- [ ] `GET /api/v1/predictions/export?format=csv` — download prediction history
- [ ] Support CSV and JSON formats
- [ ] Date range filtering

#### 27. Admin / System Management APIs
- [ ] `GET /api/v1/admin/db/stats` — table sizes, row counts
- [ ] `POST /api/v1/admin/cache/clear` — flush Redis cache
- [ ] `GET /api/v1/admin/config` — current (non-secret) config values
- [ ] Protected by admin-level API key

#### 28. Soft Delete for Predictions
- [ ] Add `deleted_at` field to `PredictionLog`
- [ ] `DELETE /api/v1/predictions/{id}` — soft delete (set `deleted_at`)
- [ ] Filter out soft-deleted records from list queries
- [ ] `GET /api/v1/admin/predictions/deleted` — view deleted records

---

## 📋 Recommended Implementation Order

### Phase 1 — Core Completeness (Do First)
| # | Task | Effort |
|---|------|--------|
| 1 | Prediction History endpoints | ~2 hrs |
| 3 | Schemas refactor | ~1 hr |
| 9 | Router modularization | ~1 hr |
| 5 | Crop_Growth_Stage enum | ~30 min |
| 2 | Latency tracking | ~30 min |

### Phase 2 — Production Hardening
| # | Task | Effort |
|---|------|--------|
| 10 | Config validation (pydantic-settings) | ~1 hr |
| 7 | HTTP connection pooling | ~1 hr |
| 4 | CORS restriction | ~30 min |
| 8 | Dockerfile hardening | ~30 min |
| 6 | Structured logging | ~1 hr |
| 18 | Request ID middleware | ~1 hr |

### Phase 3 — Security & Reliability
| # | Task | Effort |
|---|------|--------|
| 11 | Authentication | ~2 hrs |
| 12 | Rate limiting | ~1 hr |
| 15 | Retry logic | ~1 hr |
| 16 | Circuit breaker | ~2 hrs |
| 17 | DB migrations | ~1 hr |

### Phase 4 — Enhancements
| # | Task | Effort |
|---|------|--------|
| 14 | Analytics endpoints | ~2 hrs |
| 21 | Batch predictions | ~2 hrs |
| 22 | Feedback endpoint | ~1 hr |
| 19 | Comprehensive tests | ~3 hrs |
| 20 | OpenAPI docs | ~1 hr |

---

## 🗂️ Target Backend File Structure (After All Tasks)

```
backend/
├── .dockerignore                   # [NEW] Docker build exclusions
├── Dockerfile                      # [MODIFIED] Hardened with non-root user
├── requirements.txt                # [MODIFIED] Pinned versions + new deps
├── config.py                       # [MODIFIED] pydantic-settings based
├── logging_config.py               # [NEW] Structured JSON logging
├── main.py                         # [MODIFIED] Slim — app + router includes only
│
├── schemas/                        # [NEW] Pydantic models
│   ├── __init__.py
│   ├── common.py                   # ErrorResponse, PaginatedResponse
│   ├── recommendation.py           # RecommendRequest, RecommendResponse
│   └── prediction.py               # PredictionDetail, PredictionStats
│
├── routers/                        # [NEW] API route modules
│   ├── __init__.py
│   ├── recommendation.py           # POST /recommend
│   ├── predictions.py              # GET/DELETE /predictions
│   ├── analytics.py                # GET /analytics/*
│   └── system.py                   # GET /health, /ready
│
├── middleware/                     # [NEW] Middleware
│   ├── __init__.py
│   ├── auth.py                     # API key authentication
│   ├── rate_limit.py               # Rate limiting
│   └── request_id.py               # X-Request-ID propagation
│
├── database/
│   ├── __init__.py
│   ├── db.py                       # [MODIFIED] Add read/query functions
│   └── migrations/                 # [NEW] Schema migrations
│       └── 001_initial.py
│
├── services/
│   ├── __init__.py
│   ├── ml_client.py                # [MODIFIED] Connection pool, retry, circuit breaker
│   └── cache.py                    # [NEW] Redis caching layer
│
└── utils/                          # [NEW] Shared utilities
    ├── __init__.py
    └── pagination.py               # Pagination helper
```
