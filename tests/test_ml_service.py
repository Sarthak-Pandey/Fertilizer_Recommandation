import sys
import importlib.util
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Dynamically load ml-service/main.py as a distinct module to prevent collision with backend/main.py
ml_service_main_path = Path(__file__).parent.parent / "ml-service" / "main.py"
spec = importlib.util.spec_from_file_location("ml_service_main", ml_service_main_path)
ml_service_main = importlib.util.module_from_spec(spec)
sys.modules["ml_service_main"] = ml_service_main

# Add ml-service directory to sys.path so its internal imports (schemas, inference) work
ml_service_dir = str(Path(__file__).parent.parent / "ml-service")
if ml_service_dir not in sys.path:
    sys.path.insert(0, ml_service_dir)

spec.loader.exec_module(ml_service_main)

app = ml_service_main.app
client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_version" in data

def test_readiness_endpoint():
    with TestClient(app) as test_client:
        response = test_client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["model_loaded"] is True
        assert data["model_version"] == "model-v1"

def test_predict_endpoint_success():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }
    with TestClient(app) as test_client:
        response = test_client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "fertilizer" in data
        assert isinstance(data["fertilizer"], str)
        assert data["model_version"] == "model-v1"
        assert data["confidence"] is not None
        assert 0.0 <= data["confidence"] <= 1.0
        assert "probabilities" in data

def test_predict_endpoint_invalid_features():
    payload = {
        "Soil_pH": 6.5,
        # Missing Nitrogen_Level
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }
    with TestClient(app) as test_client:
        response = test_client.post("/predict", json=payload)
        assert response.status_code == 422
