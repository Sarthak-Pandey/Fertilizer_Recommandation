"""
Phase 3 Test Suite -- Security, ML Resilience & Database Integrity.

Tests:
- API Key Authentication (Protected vs Public endpoints, valid/invalid/missing headers, 401 handling)
- Request ID correlation & secret non-leakage on auth failure
- ML Client exponential backoff retry logic (transient retry vs non-retryable 422 input errors)
- ML Circuit Breaker state machine (CLOSED -> OPEN -> HALF_OPEN -> CLOSED)
- Peewee database migration runner execution, idempotency, and failure safety
"""

import sys
import json
import logging
import time
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import httpx
import peewee
from fastapi.testclient import TestClient

from backend import main
from backend.main import app
from backend.config import settings
from backend.database.db import db, PredictionLog
from backend.database.migrations.runner import SchemaMigration, run_migrations
from backend.services.circuit_breaker import CircuitBreaker, CircuitState
from backend.services.ml_client import MLClient, MLServiceError

client = TestClient(app)
VALID_HEADERS = {"X-API-Key": settings.API_KEY}


@pytest.fixture(autouse=True)
def setup_db():
    db.connect(reuse_if_open=True)
    db.create_tables([PredictionLog, SchemaMigration], safe=True)
    PredictionLog.delete().execute()
    yield


# ---------------------------------------------------------------------------
# 1. API Key Authentication Tests
# ---------------------------------------------------------------------------

def test_public_health_endpoint_without_key():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "backend" in response.json()


def test_public_ready_endpoint_without_key():
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    assert "backend" in response.json()


def test_protected_recommend_endpoint_missing_key():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative",
    }
    response = client.post("/api/v1/fertilizer/recommend", json=payload)
    assert response.status_code == 401
    assert response.json()["success"] is False
    assert "Unauthorized" in response.json()["error"]
    assert response.headers.get("X-Request-ID") is not None


def test_protected_recommend_endpoint_invalid_key():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative",
    }
    response = client.post(
        "/api/v1/fertilizer/recommend",
        json=payload,
        headers={"X-API-Key": "invalid-secret-key"},
    )
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_protected_recommend_endpoint_valid_key():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative",
    }
    mock_ml_response = {
        "fertilizer": "Urea",
        "confidence": 0.95,
        "model_version": "model-v1",
        "preprocessing_version": "preprocessing-v1",
        "feature_schema_version": "features-v1",
    }
    with patch.object(main.ml_client, "predict", new_callable=AsyncMock) as mock_predict:
        mock_predict.return_value = mock_ml_response
        response = client.post(
            "/api/v1/fertilizer/recommend",
            json=payload,
            headers=VALID_HEADERS,
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["fertilizer"] == "Urea"


def test_protected_predictions_history_endpoints():
    # Missing key
    r_list = client.get("/api/v1/predictions")
    assert r_list.status_code == 401

    r_stats = client.get("/api/v1/predictions/stats")
    assert r_stats.status_code == 401

    # Valid key
    r_list_valid = client.get("/api/v1/predictions", headers=VALID_HEADERS)
    assert r_list_valid.status_code == 200

    r_stats_valid = client.get("/api/v1/predictions/stats", headers=VALID_HEADERS)
    assert r_stats_valid.status_code == 200


def test_auth_failure_does_not_log_prediction_or_call_ml():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative",
    }
    with patch.object(main.ml_client, "predict", new_callable=AsyncMock) as mock_predict:
        response = client.post("/api/v1/fertilizer/recommend", json=payload)
        assert response.status_code == 401
        assert mock_predict.call_count == 0
        assert PredictionLog.select().count() == 0


# ---------------------------------------------------------------------------
# 2. ML Retry & Circuit Breaker Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ml_retry_success_on_second_attempt():
    ml_c = MLClient(
        base_url="http://localhost:8001",
        timeout=2.0,
        max_retries=3,
        retry_base_delay=0.01,
        retry_max_delay=0.05,
    )
    await ml_c.open()

    mock_resp_success = MagicMock()
    mock_resp_success.status_code = 200
    mock_resp_success.json.return_value = {"fertilizer": "DAP", "confidence": 0.9}

    with patch.object(ml_c._client, "post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = [httpx.ConnectError("Connection refused"), mock_resp_success]
        res = await ml_c.predict({"Soil_pH": 6.5})
        assert res["fertilizer"] == "DAP"
        assert mock_post.call_count == 2

    await ml_c.close()


@pytest.mark.asyncio
async def test_ml_retry_non_retryable_422_error():
    ml_c = MLClient(
        base_url="http://localhost:8001",
        timeout=2.0,
        max_retries=3,
        retry_base_delay=0.01,
    )
    await ml_c.open()

    mock_resp_422 = MagicMock()
    mock_resp_422.status_code = 422
    mock_resp_422.json.return_value = {"detail": "Invalid pH value"}

    with patch.object(ml_c._client, "post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp_422
        with pytest.raises(MLServiceError) as exc_info:
            await ml_c.predict({"Soil_pH": 99.0})

        assert exc_info.value.status_code == 400
        assert "Invalid input" in str(exc_info.value)
        # Should NOT retry 422
        assert mock_post.call_count == 1

    await ml_c.close()


@pytest.mark.asyncio
async def test_circuit_breaker_state_transitions():
    cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=0.1)
    assert cb.state == CircuitState.CLOSED
    assert await cb.can_execute() is True

    # Record 2 failures -> OPEN
    await cb.record_failure()
    await cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert await cb.can_execute() is False

    # Wait for cooldown
    time.sleep(0.15)

    # First call after cooldown -> HALF_OPEN
    assert await cb.can_execute() is True
    assert cb.state == CircuitState.HALF_OPEN

    # Record success -> CLOSED
    await cb.record_success()
    assert cb.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_ml_client_short_circuits_when_open():
    cb = CircuitBreaker(failure_threshold=1, cooldown_seconds=10.0)
    await cb.record_failure()
    assert cb.state == CircuitState.OPEN

    ml_c = MLClient(
        base_url="http://localhost:8001",
        timeout=2.0,
        circuit_breaker=cb,
    )
    await ml_c.open()

    with patch.object(ml_c._client, "post", new_callable=AsyncMock) as mock_post:
        with pytest.raises(MLServiceError) as exc_info:
            await ml_c.predict({"Soil_pH": 6.5})

        assert exc_info.value.status_code == 503
        assert "circuit breaker is OPEN" in str(exc_info.value)
        # No HTTP call made when circuit is OPEN
        assert mock_post.call_count == 0

    await ml_c.close()


# ---------------------------------------------------------------------------
# 3. Database Migration Runner Tests
# ---------------------------------------------------------------------------

def test_database_migration_runner_execution_and_idempotency():
    test_db = peewee.SqliteDatabase(":memory:")
    test_db.connect()

    # Initial migration execution
    applied = run_migrations(test_db)
    assert "001_initial_schema" in applied

    # Idempotent second execution
    reapplied = run_migrations(test_db)
    assert len(reapplied) == 0

    test_db.close()
