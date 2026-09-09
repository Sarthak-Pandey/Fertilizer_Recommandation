"""
Phase 2 Test Suite -- Operational Hardening & Production Foundations.

Tests:
- pydantic-settings config validation (ML_SERVICE_URL, ML_REQUEST_TIMEOUT, ALLOWED_ORIGINS)
- Persistent MLClient connection pooling (lifecycle open/close & client reuse)
- Environment-restricted CORS policy
- Request ID / correlation ID middleware (preservation, generation, header & log correlation)
- Structured logging formatters (JSON & Human-readable)
"""

import sys
import json
import logging
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch

root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend import main
from backend.main import app
from backend.config import Settings
from backend.database.db import db, PredictionLog
from backend.services.ml_client import MLClient, MLServiceError
from backend.logging_config import StructuredJSONFormatter, HumanReadableFormatter
from backend.middleware.request_id import request_id_ctx_var, get_request_id

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    db.connect(reuse_if_open=True)
    db.create_tables([PredictionLog], safe=True)
    PredictionLog.delete().execute()
    yield
    db.close()


# ---------------------------------------------------------------------------
# 1. Configuration Validation Tests
# ---------------------------------------------------------------------------

def test_config_valid_defaults():
    s = Settings()
    assert s.ML_SERVICE_URL == "http://localhost:8001"
    assert s.ML_REQUEST_TIMEOUT == 10.0
    assert "http://localhost:3000" in s.ALLOWED_ORIGINS
    assert "http://localhost:5173" in s.ALLOWED_ORIGINS


def test_config_invalid_ml_url():
    with pytest.raises(ValidationError) as exc_info:
        Settings(ML_SERVICE_URL="ftp://localhost:8001")
    assert "ML_SERVICE_URL must start with http:// or https://" in str(exc_info.value)


@pytest.mark.parametrize("invalid_timeout", [0.0, -5.0])
def test_config_invalid_ml_timeout(invalid_timeout):
    with pytest.raises(ValidationError) as exc_info:
        Settings(ML_REQUEST_TIMEOUT=invalid_timeout)
    assert "ML_REQUEST_TIMEOUT must be greater than 0" in str(exc_info.value)


def test_config_allowed_origins_comma_separated():
    s = Settings(ALLOWED_ORIGINS="http://app.domain.com, https://admin.domain.com")
    assert s.ALLOWED_ORIGINS == ["http://app.domain.com", "https://admin.domain.com"]


# ---------------------------------------------------------------------------
# 2. Connection Pooling Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ml_client_connection_pooling_lifecycle():
    ml_c = MLClient(base_url="http://localhost:8001", timeout=5.0)
    assert ml_c._client is None

    # Open pool
    await ml_c.open()
    assert ml_c._client is not None
    assert not ml_c._client.is_closed
    initial_client = ml_c._client

    # Subsequent _get_client calls reuse the exact same AsyncClient instance
    reused_client = ml_c._get_client()
    assert reused_client is initial_client

    # Close pool
    await ml_c.close()
    assert ml_c._client is None


# ---------------------------------------------------------------------------
# 3. CORS Restriction Tests
# ---------------------------------------------------------------------------

def test_cors_allowed_origin():
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_disallowed_origin():
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://malicious-domain.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Disallowed origin does not get Access-Control-Allow-Origin header matching the origin
    assert response.headers.get("access-control-allow-origin") != "http://malicious-domain.com"


# ---------------------------------------------------------------------------
# 4. Request ID Middleware & Correlation Tests
# ---------------------------------------------------------------------------

def test_request_id_preservation():
    custom_id = "client-req-99999"
    response = client.get("/api/v1/health", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_id


def test_request_id_generation_when_missing():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    generated_id = response.headers.get("X-Request-ID")
    assert generated_id is not None
    assert len(generated_id) > 10


def test_request_id_correlated_in_prediction_log():
    custom_id = "corr-req-7777"
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
            headers={"X-Request-ID": custom_id, "X-API-Key": Settings().API_KEY},
        )
        assert response.status_code == 200
        assert response.headers.get("X-Request-ID") == custom_id

        pred_id = response.json()["prediction_id"]
        log_entry = PredictionLog.get_or_none(PredictionLog.prediction_id == pred_id)
        assert log_entry is not None
        assert log_entry.request_id == custom_id


# ---------------------------------------------------------------------------
# 5. Structured Logging Tests
# ---------------------------------------------------------------------------

def test_structured_json_formatter():
    token = request_id_ctx_var.set("test-log-req-123")
    try:
        formatter = StructuredJSONFormatter()
        record = logging.LogRecord(
            name="backend.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Testing JSON log output",
            args=(),
            exc_info=None,
        )
        formatted_json = formatter.format(record)
        parsed = json.loads(formatted_json)

        assert parsed["level"] == "INFO"
        assert parsed["logger"] == "backend.test"
        assert parsed["message"] == "Testing JSON log output"
        assert parsed["request_id"] == "test-log-req-123"
        assert "timestamp" in parsed
    finally:
        request_id_ctx_var.reset(token)


def test_human_readable_formatter():
    token = request_id_ctx_var.set("test-human-req-456")
    try:
        formatter = HumanReadableFormatter(fmt="%(levelname)s %(message)s")
        record = logging.LogRecord(
            name="backend.test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=20,
            msg="Testing human log output",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "WARNING Testing human log output request_id=test-human-req-456" in formatted
    finally:
        request_id_ctx_var.reset(token)
