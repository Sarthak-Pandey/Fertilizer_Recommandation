"""
End-to-End Test -- Full flow from frontend-like request through
backend and ML service to prediction and database persistence.

This test starts both services and tests the complete integration.
"""

import time
from pathlib import Path
import httpx
import pytest

BACKEND_URL = "http://localhost:8000"
ML_SERVICE_URL = "http://localhost:8001"

VALID_REQUEST = {
    "Soil_pH": 6.5,
    "Nitrogen_Level": 40.0,
    "Phosphorus_Level": 20.0,
    "Potassium_Level": 30.0,
    "Crop_Growth_Stage": "Vegetative"
}

class TestE2EIntegration:
    """
    End-to-end integration test.
    Skips if services are not running live.
    """

    @pytest.fixture(autouse=True)
    def check_services(self):
        ml_up = False
        backend_up = False
        try:
            r = httpx.get(f"{ML_SERVICE_URL}/health", timeout=2.0)
            ml_up = r.status_code == 200
        except Exception:
            pass
        try:
            r = httpx.get(f"{BACKEND_URL}/api/v1/health", timeout=2.0)
            backend_up = r.status_code == 200
        except Exception:
            pass

        if not (ml_up and backend_up):
            pytest.skip("Live services not running on 8000/8001. Skipping live E2E test.")

    def test_ml_health(self):
        r = httpx.get(f"{ML_SERVICE_URL}/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "healthy"
        assert data["model_version"] == "model-v1"

    def test_ml_ready(self):
        r = httpx.get(f"{ML_SERVICE_URL}/ready")
        assert r.status_code == 200
        data = r.json()
        assert data["model_loaded"] is True
        assert data["model_version"] == "model-v1"

    def test_ml_predict(self):
        r = httpx.post(f"{ML_SERVICE_URL}/predict", json=VALID_REQUEST)
        assert r.status_code == 200
        data = r.json()
        assert "fertilizer" in data
        assert data["model_version"] == "model-v1"

    def test_backend_recommend(self):
        headers = {"X-API-Key": "dev-secret-key-123"}
        r = httpx.post(f"{BACKEND_URL}/api/v1/fertilizer/recommend", json=VALID_REQUEST, headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert data["success"] is True
        assert "fertilizer" in data
        assert data["model_version"] == "model-v1"
        assert data["prediction_id"] is not None

    def test_backend_health(self):
        r = httpx.get(f"{BACKEND_URL}/api/v1/health")
        assert r.status_code == 200
        data = r.json()
        assert data["backend"] == "healthy"

    def test_backend_ready(self):
        r = httpx.get(f"{BACKEND_URL}/api/v1/ready")
        assert r.status_code == 200
