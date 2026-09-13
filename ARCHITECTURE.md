# System Architecture & Component Structure
## Fertilizer Recommendation System

---

## Executive Summary

The **Fertilizer Recommendation System** is designed following clean architecture, microservices separation of concerns, and resilient distributed systems principles. The platform decouples request routing, authentication, validation, and persistent auditing (**Backend Gateway Service**) from computationally intensive machine learning inference (**ML Inference Service**).

---

## Table of Contents

1. [High-Level Microservices Architecture](#1-high-level-microservices-architecture)
2. [End-to-End Request/Response Sequence](#2-end-to-end-requestresponse-sequence)
3. [Fault Tolerance & Circuit Breaker State Machine](#3-fault-tolerance--circuit-breaker-state-machine)
4. [Database ERD & Storage Schema](#4-database-erd--storage-schema)
5. [Machine Learning Inference Pipeline](#5-machine-learning-inference-pipeline)
6. [Complete Codebase & Directory Structure](#6-complete-codebase--directory-structure)

---

## 1. High-Level Microservices Architecture

The system consists of two primary Dockerized microservices connected over a isolated virtual bridge network (`backend_net`), backed by a persistent relational database and Prometheus metrics instrumentation:

```mermaid
graph TD
    Client([Farmer / Mobile / Web Client]) -->|HTTP REST / JSON| Gateway[FastAPI Gateway :8000]

    subgraph Gateway Middleware Stack [Gateway Middleware Stack]
        Gateway --> ID[1. X-Request-ID Injector]
        ID --> CORS[2. CORS Restriction Policy]
        CORS --> Auth[3. X-API-Key Auth Check]
        Auth --> Rate[4. Rate Limiter Middleware]
    end

    subgraph Router & Resiliency Layer [Gateway Core & Resiliency]
        Rate --> Router[FastAPI Routers]
        Router --> CB{Circuit Breaker}
        CB -->|CLOSED / HALF_OPEN| Retry[Exponential Backoff Retry Engine]
        CB -->|OPEN| Fallback[Fast Fallback Response :503]
        Retry -->|Persistent Async HTTP Pool| MLClient[ML HTTP Client]
    end

    subgraph ML Microservice Stack [ML Inference Microservice :8001]
        MLClient -->|POST /predict| MLServer[FastAPI ML Engine]
        MLServer --> Preproc[StandardScaler Preprocessor]
        Preproc --> XGB[XGBoost Classifier]
        Preproc --> RF[Random Forest Classifier]
        XGB --> Ensemble[Multi-Class Probability Aggregator]
        RF --> Ensemble
    end

    subgraph Persistence & Observability Layer [Persistence & Observability]
        Router -->|Async Audit Log| DB[(SQLite / PostgreSQL DB)]
        Gateway -->|Scrape Endpoint| Prom[Prometheus Engine /metrics]
        Gateway --> Logs[Structured JSON Logger]
    end
```

---

## 2. End-to-End Request/Response Sequence

The sequence diagram below traces a prediction request from client initiation through authentication, resiliency checks, ML inference execution, database auditing, and telemetry emission:

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client App / Agronomist
    participant MW as Gateway Middleware Stack
    participant Router as Recommendation Router
    participant CB as Circuit Breaker & Retry Engine
    participant ML as ML Inference Service (:8001)
    participant DB as Database (Peewee ORM)

    Client->>MW: POST /api/v1/fertilizer/recommend (X-API-Key, Soil Features)
    MW->>MW: Inject X-Request-ID & Verify X-API-Key Header
    alt Authentication Failure
        MW-->>Client: 401 Unauthorized Response
    else Authentication Success
        MW->>Router: Handover Validated HTTP Request
        Router->>Router: Pydantic Schema Validation (Soil_pH, N, P, K, Growth Stage)
        alt Validation Failure
            Router-->>Client: 422 Unprocessable Entity
        else Validation Success
            Router->>CB: Execute ML Service Prediction Request
            alt Circuit Breaker == OPEN
                CB-->>Router: MLServiceError (Circuit Breaker OPEN)
                Router-->>Client: 503 Service Unavailable (Fast Fallback)
            else Circuit Breaker == CLOSED / HALF_OPEN
                loop Retry Loop (Up to max_retries = 3)
                    CB->>ML: POST /predict (Features)
                    alt ML Response HTTP 200 OK
                        ML-->>CB: JSON {fertilizer, confidence, probabilities, model_version}
                    else ML Transient Failure (503/504/ConnectError)
                        ML-->>CB: Network Error or Server Error
                        CB->>CB: Sleep (base_delay * 2^attempt + jitter)
                    end
                end
                alt Retries Succeeded
                    CB->>CB: Record Success (Reset Failure Counter / Close Circuit)
                    CB-->>Router: Prediction Result Dict
                    Router->>DB: Log Prediction Audit Record (async non-blocking)
                    DB-->>Router: Return prediction_id (UUID)
                    Router-->>Client: HTTP 200 OK Response (Fertilizer, Confidence, Latency)
                else Retries Exhausted
                    CB->>CB: Record Failure (Increment Counter / Trip to OPEN)
                    CB-->>Router: Raise MLServiceError (503/504)
                    Router-->>DB: Log Failed Prediction Record
                    Router-->>Client: HTTP 503/504 Error Response
                end
            end
        end
    end
```

---

## 3. Fault Tolerance & Circuit Breaker State Machine

To protect the Gateway from cascading outages during ML service maintenance or degradation, a state-machine Circuit Breaker is maintained in memory:

```mermaid
stateDiagram-v2
    [*] --> CLOSED : Service Initialization

    state CLOSED {
        [*] --> MonitoringClosed
        MonitoringClosed --> MonitoringClosed : Normal Operation (Success)
        MonitoringClosed --> FailureCountInc : Connection / HTTP 5xx Error
    }

    CLOSED --> OPEN : Consecutive Failures >= 5

    state OPEN {
        [*] --> CooldownTimer
        CooldownTimer --> CooldownTimer : Reject Requests (Fast 503 Return)
    }

    OPEN --> HALF_OPEN : Cooldown Period (30s) Expired

    state HALF_OPEN {
        [*] --> ProbeExecution
        ProbeExecution --> ProbeSuccess : Test Request Succeeded
        ProbeExecution --> ProbeFailure : Test Request Failed
    }

    HALF_OPEN --> CLOSED : 2 Consecutive Successful Probes
    HALF_OPEN --> OPEN : Single Probe Failure
```

---

## 4. Database ERD & Storage Schema

All predictions are recorded in an audit table (`prediction_logs`) using Peewee ORM to support historical lookups, paginated dashboard queries, aggregated metrics, and machine learning retraining audits.

```mermaid
erDiagram
    PREDICTION_LOGS {
        string prediction_id PK "UUID Primary Key"
        string request_id FK "Distributed Correlation Request ID (Indexed)"
        string input_features "Raw JSON String of Input Features"
        string predicted_fertilizer "Recommended Fertilizer Name"
        string gate_decision "Gating decision tag (default: N/A)"
        string specialist_used "Model Classifier used"
        float confidence "Model Prediction Probability (0.0 - 1.0)"
        string model_version "ML Model Version Tag (Indexed)"
        string preprocessing_version "Preprocessor Artifact Tag"
        string feature_schema_version "Feature Pipeline Version Tag"
        float latency_ms "Total Execution Time in Milliseconds"
        string status "Operation Status (success | error)"
        string error_message "Error Details if status == error"
        datetime created_at "UTC Timestamp of Prediction"
    }
```

---

## 5. Machine Learning Inference Pipeline

The ML pipeline ingests numerical soil properties and categorical growth stages, transforms features, feeds them through an ensemble classification engine, and outputs normalized class confidence distributions:

```mermaid
flowchart LR
    subgraph Raw Input Data
        pH[Soil pH: 0.0 - 14.0]
        N[Nitrogen Level: mg/kg]
        P[Phosphorus Level: mg/kg]
        K[Potassium Level: mg/kg]
        Stage[Growth Stage: Sowing/Vegetative/Flowering/Harvest]
    end

    subgraph Preprocessing & Feature Pipeline
        pH & N & P & K --> Impute[Numeric Imputer & RobustScaler]
        Stage --> OneHot[One-Hot Encoder]
        Impute & OneHot --> FeatureVector[Dense Feature Vector]
    end

    subgraph Ensemble Inference Engine
        FeatureVector --> XGB[XGBoost Classifier]
        FeatureVector --> RF[Random Forest Classifier]
        XGB --> ProbXGB[Class Probability Vector]
        RF --> ProbRF[Class Probability Vector]
        ProbXGB & ProbRF --> Ensemble[Soft-Voting Weighted Aggregator]
    end

    subgraph Inference Output
        Ensemble --> TopClass[Predicted Fertilizer Label]
        Ensemble --> Conf[Confidence Score]
        Ensemble --> Map[Class Probabilities Map]
    end
```

---

## 6. Complete Codebase & Directory Structure

The visual hierarchy below details how code files are organized across microservice modules:

```text
Fertilizer_Recommend/
│
├── 📁 backend/                       # API Gateway FastAPI Microservice (:8000)
│   ├── 📄 main.py                    # Application entrypoint, CORS, Router mounting & lifespan
│   ├── 📄 config.py                  # Environment settings validation via pydantic-settings
│   ├── 📄 logging_config.py          # Structured JSON logging formatter & correlation engine
│   ├── 📄 Dockerfile                 # Hardened non-root Python 3.13 image for Gateway
│   │
│   ├── 📁 database/                  # Database Layer (Peewee ORM)
│   │   ├── 📄 db.py                  # PredictionLog model, connection manager & query helpers
│   │   └── 📁 migrations/            # Database schema migration engine & scripts
│   │       ├── 📄 runner.py          # Version tracking & migration execution logic
│   │       └── 📄 001_initial.py     # Initial schema creation script
│   │
│   ├── 📁 middleware/                # FastAPI Custom HTTP Middleware
│   │   ├── 📄 auth.py                # Header-based X-API-Key authentication policy
│   │   ├── 📄 request_id.py          # Distributed tracing X-Request-ID generation/propagation
│   │   └── 📄 rate_limit.py          # Sliding-window in-memory IP rate limiter
│   │
│   ├── 📁 routers/                   # REST API Endpoint Controllers
│   │   ├── 📄 recommendation.py      # POST /api/v1/fertilizer/recommend handler
│   │   ├── 📄 predictions.py         # GET /api/v1/predictions history & stats handlers
│   │   └── 📄 health.py              # GET /api/v1/health & readiness checks
│   │
│   ├── 📁 schemas/                   # Pydantic v2 Request/Response Data Validation
│   │   ├── 📄 recommendation.py      # RecommendRequest & RecommendResponse models
│   │   ├── 📄 prediction.py          # PredictionDetail & PredictionListResponse models
│   │   └── 📄 common.py              # Common API response wrappers & Error schemas
│   │
│   ├── 📁 services/                  # Business Logic & External Service Integration
│   │   ├── 📄 ml_client.py           # Resilient HTTP Client (Persistent Pool, Retries)
│   │   └── 📄 circuit_breaker.py     # Thread-safe Circuit Breaker state machine
│   │
│   └── 📁 utils/                     # Utility Helper Functions
│       ├── 📄 telemetry.py           # Prometheus metrics exporter (/metrics)
│       └── 📄 pagination.py         # Database pagination calculation helpers
│
├── 📁 ml-service/                    # ML Inference Microservice (:8001)
│   ├── 📄 main.py                    # FastAPI application exposing POST /predict & /health
│   ├── 📄 Dockerfile                 # Container setup for ML inference microservice
│   │
│   ├── 📁 inference/                 # Core Prediction Logic
│   │   ├── 📄 predictor.py           # Model loader & vectorized inference executor
│   │   └── 📄 preprocessor.py        # Feature scaling & One-Hot encoding transformer
│   │
│   ├── 📁 models/                    # Serialized Machine Learning Artifacts
│   │   └── 📁 model-v1/              # XGBoost/RF pickle artifacts & metadata JSON
│   │
│   └── 📁 schemas/                   # Data contracts for internal ML requests
│
├── 📁 training/                      # Machine Learning Training Pipeline
│   ├── 📄 train.py                   # Model training, hyperparameter tuning & artifact export
│   └── 📁 data/                      # Raw & processed agricultural soil datasets
│
├── 📁 tests/                         # Comprehensive Pytest Suite
│   ├── 📄 test_recommendation.py     # End-to-end API recommendation tests
│   ├── 📄 test_predictions_api.py    # Prediction history & pagination tests
│   ├── 📄 test_circuit_breaker.py    # Resilience & fallback unit tests
│   └── 📄 test_ml_client.py         # Async HTTP client retry tests
│
├── 📄 docker-compose.yml             # Multi-container orchestrator configuration
├── 📄 .env.example                   # Environment configuration template
├── 📄 SRS.md                         # Software Requirements Specification (IEEE 830)
├── 📄 ARCHITECTURE.md                # System Architecture & Diagram Specifications (This document)
└── 📄 README.md                      # General project overview & setup guide
```
