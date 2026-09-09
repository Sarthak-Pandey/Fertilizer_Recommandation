import sys
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend import main
from backend.config import settings
from backend.main import app
from backend.database.db import log_prediction, PredictionLog, db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    db.connect(reuse_if_open=True)
    db.create_tables([PredictionLog], safe=True)
    yield
    db.close()

def test_recommend_endpoint_success():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }

    mock_ml_response = {
        "fertilizer": "Urea",
        "confidence": 0.9998,
        "model_version": "model-v1",
        "preprocessing_version": "preprocessing-v1",
        "feature_schema_version": "features-v1",
        "probabilities": {"Urea": 0.9998, "DAP": 0.0002}
    }

    with patch.object(main.ml_client, "predict", new_callable=AsyncMock) as mock_predict:
        mock_predict.return_value = mock_ml_response
        response = client.post("/api/v1/fertilizer/recommend", json=payload, headers={"X-API-Key": settings.API_KEY})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["fertilizer"] == "Urea"
        assert data["confidence"] == 0.9998
        assert data["model_version"] == "model-v1"
        assert "prediction_id" in data

def test_backend_health_and_ready():
    with patch.object(main.ml_client, "health", new_callable=AsyncMock) as mock_health, \
         patch.object(main.ml_client, "ready", new_callable=AsyncMock) as mock_ready:
        mock_health.return_value = {"status": "healthy", "model_version": "model-v1"}
        mock_ready.return_value = {"status": "ready", "model_loaded": True, "model_version": "model-v1"}

        h_resp = client.get("/api/v1/health")
        assert h_resp.status_code == 200
        assert h_resp.json()["backend"] == "healthy"

        r_resp = client.get("/api/v1/ready")
        assert r_resp.status_code == 200
        assert r_resp.json()["backend"] == "ready"
