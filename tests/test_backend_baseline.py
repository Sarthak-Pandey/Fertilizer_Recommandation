"""
Phase 0 — Backend Baseline Test Suite

Verifies existing behavior of backend FastAPI application prior to Phase 1 refactoring:
- Recommendation endpoint (success, input validation failures, ML service failure handling)
- Health and readiness endpoints
- Database persistence and peewee log handling (latency_ms check, error handling)
"""

import sys
import math
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Ensure root workspace and backend package are importable
root_dir = str(Path(__file__).parent.parent)
backend_dir = str(Path(__file__).parent.parent / "backend")
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from backend import main
from backend.config import settings
from backend.main import app
from backend.database.db import db, PredictionLog, log_prediction
from backend.services.ml_client import MLServiceError

client = TestClient(app, headers={"X-API-Key": settings.API_KEY})


@pytest.fixture(autouse=True)
def setup_db():
    db.connect(reuse_if_open=True)
    db.create_tables([PredictionLog], safe=True)
    yield
    db.close()


# ---------------------------------------------------------------------------
# 1. Recommendation Endpoint — Success & Data Flow
# ---------------------------------------------------------------------------

def test_recommend_success():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }

    mock_ml_response = {
        "fertilizer": "Urea",
        "confidence": 0.95,
        "model_version": "model-v1",
        "preprocessing_version": "preprocessing-v1",
        "feature_schema_version": "features-v1",
        "probabilities": {"Urea": 0.95, "DAP": 0.05}
    }

    with patch.object(main.ml_client, "predict", new_callable=AsyncMock) as mock_predict:
        mock_predict.return_value = mock_ml_response
        response = client.post("/api/v1/fertilizer/recommend", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["fertilizer"] == "Urea"
        assert data["confidence"] == 0.95
        assert data["model_version"] == "model-v1"
        assert data["preprocessing_version"] == "preprocessing-v1"
        assert data["feature_schema_version"] == "features-v1"
        assert data["prediction_id"] is not None
        assert data["probabilities"] == {"Urea": 0.95, "DAP": 0.05}

        # Verify DB persistence
        log_entry = PredictionLog.get_or_none(PredictionLog.prediction_id == data["prediction_id"])
        assert log_entry is not None
        assert log_entry.predicted_fertilizer == "Urea"
        assert log_entry.confidence == 0.95
        assert log_entry.model_version == "model-v1"
        assert log_entry.status == "success"
        # Confirm latency_ms is measured and populated in Phase 1
        assert log_entry.latency_ms is not None
        assert isinstance(log_entry.latency_ms, float)



# ---------------------------------------------------------------------------
# 2. Input Validation Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_ph", [-1.0, 14.1, 100.0])
def test_recommend_invalid_ph(invalid_ph):
    payload = {
        "Soil_pH": invalid_ph,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }
    response = client.post("/api/v1/fertilizer/recommend", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize("field,value", [
    ("Nitrogen_Level", -5.0),
    ("Phosphorus_Level", -10.0),
    ("Potassium_Level", -0.1),
])
def test_recommend_negative_numeric_values(field, value):
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }
    payload[field] = value
    response = client.post("/api/v1/fertilizer/recommend", json=payload)
    assert response.status_code == 422


def test_recommend_missing_required_fields():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0
        # Missing Phosphorus, Potassium, Crop_Growth_Stage
    }
    response = client.post("/api/v1/fertilizer/recommend", json=payload)
    assert response.status_code == 422


def test_recommend_malformed_json():
    response = client.post(
        "/api/v1/fertilizer/recommend",
        content="not-json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# 3. ML Service Error Handling Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("error_status_code,error_msg,expected_api_status", [
    (503, "ML service is unavailable", 503),
    (504, "ML service request timed out after 10s", 504),
    (502, "ML service HTTP error: ...", 502),
    (400, "Invalid input: validation error", 400),
    (500, "ML prediction failed: internal ML crash", 500),
])
def test_recommend_ml_failure_modes(error_status_code, error_msg, expected_api_status):
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }

    with patch.object(main.ml_client, "predict", new_callable=AsyncMock) as mock_predict:
        mock_predict.side_effect = MLServiceError(error_msg, status_code=error_status_code)
        response = client.post("/api/v1/fertilizer/recommend", json=payload)
        
        assert response.status_code == expected_api_status
        assert error_msg in response.json()["detail"]

        # Confirm that ML failure logs prediction with status="error"
        error_logs = list(PredictionLog.select().where(PredictionLog.status == "error"))
        assert len(error_logs) >= 1
        latest_error = error_logs[-1]
        assert latest_error.predicted_fertilizer == "N/A"
        assert latest_error.error_message == error_msg


# ---------------------------------------------------------------------------
# 4. Health and Readiness Endpoints
# ---------------------------------------------------------------------------

def test_health_endpoint_healthy_ml():
    mock_ml_health = {"status": "healthy", "model_version": "model-v1"}
    with patch.object(main.ml_client, "health", new_callable=AsyncMock) as mock_health:
        mock_health.return_value = mock_ml_health
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["backend"] == "healthy"
        assert data["ml_service"] == mock_ml_health


def test_health_endpoint_unreachable_ml():
    mock_ml_health = {"status": "unreachable", "error": "Connection refused"}
    with patch.object(main.ml_client, "health", new_callable=AsyncMock) as mock_health:
        mock_health.return_value = mock_ml_health
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["backend"] == "healthy"
        assert data["ml_service"]["status"] == "unreachable"


def test_ready_endpoint_ready_ml():
    mock_ml_ready = {"status": "ready", "model_loaded": True, "model_version": "model-v1"}
    with patch.object(main.ml_client, "ready", new_callable=AsyncMock) as mock_ready:
        mock_ready.return_value = mock_ml_ready
        response = client.get("/api/v1/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["backend"] == "ready"
        assert data["ml_service"] == mock_ml_ready


def test_ready_endpoint_unreachable_ml():
    mock_ml_ready = {"status": "unreachable", "model_loaded": False, "error": "Connection refused"}
    with patch.object(main.ml_client, "ready", new_callable=AsyncMock) as mock_ready:
        mock_ready.return_value = mock_ml_ready
        response = client.get("/api/v1/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["backend"] == "ready"
        assert data["ml_service"]["model_loaded"] is False


# ---------------------------------------------------------------------------
# 5. Database Resilience & Latency Inspection
# ---------------------------------------------------------------------------

def test_log_prediction_db_failure_does_not_crash():
    """Verify log_prediction catches DB errors gracefully and returns prediction_id."""
    with patch.object(PredictionLog, "create", side_effect=Exception("Database lock error")):
        pred_id = log_prediction(
            input_features={"Soil_pH": 6.5},
            predicted_fertilizer="Urea",
            model_version="model-v1",
            preprocessing_version="preprocessing-v1",
            feature_schema_version="features-v1",
            status="success"
        )
        assert isinstance(pred_id, str)
        assert len(pred_id) > 0


def test_recommend_endpoint_db_failure_resilience():
    """Verify backend returns HTTP 200 success response even if DB write fails."""
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }

    mock_ml_response = {
        "fertilizer": "Urea",
        "confidence": 0.95,
        "model_version": "model-v1",
        "preprocessing_version": "preprocessing-v1",
        "feature_schema_version": "features-v1",
    }

    with patch.object(main.ml_client, "predict", new_callable=AsyncMock) as mock_predict, \
         patch.object(PredictionLog, "create", side_effect=Exception("DB Disk Full")):
        mock_predict.return_value = mock_ml_response
        response = client.post("/api/v1/fertilizer/recommend", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["fertilizer"] == "Urea"
        assert data["prediction_id"] is not None
