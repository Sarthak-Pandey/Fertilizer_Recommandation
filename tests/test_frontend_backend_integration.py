"""
Integration Test Suite -- Frontend API Service <-> Backend API Gateway

Tests all endpoints consumed by frontend/src/services/api.ts to ensure 
complete contract compatibility between Frontend and Backend Gateway.

Run with:
    pytest tests/test_frontend_backend_integration.py -v
"""

import httpx
import pytest

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"
API_KEY = "dev-secret-key-123"

HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
}

SAMPLE_RECOMMENDATION_PAYLOAD = {
    "Soil_pH": 6.5,
    "Nitrogen_Level": 40.0,
    "Phosphorus_Level": 20.0,
    "Potassium_Level": 30.0,
    "Crop_Growth_Stage": "Vegetative",
}


@pytest.fixture(scope="module")
def http_client():
    with httpx.Client(timeout=10.0) as client:
        yield client


class TestFrontendBackendIntegration:
    """Test suite matching all API calls defined in frontend/src/services/api.ts"""

    def test_frontend_server_routes(self, http_client):
        """Verify Vite frontend server is up and serving routes / and /overview."""
        try:
            r_root = http_client.get(f"{FRONTEND_URL}/")
            assert r_root.status_code == 200, f"Frontend root / returned {r_root.status_code}"

            r_overview = http_client.get(f"{FRONTEND_URL}/overview")
            assert r_overview.status_code == 200, f"Frontend /overview returned {r_overview.status_code}"
        except httpx.ConnectError:
            pytest.fail("Frontend dev server is not running on http://localhost:5173")

    def test_api_get_system_health(self, http_client):
        """Matches frontend api.getSystemHealth() -> GET /api/v1/health"""
        r = http_client.get(f"{BACKEND_URL}/api/v1/health")
        assert r.status_code == 200, f"Health check failed with status {r.status_code}"
        data = r.json()
        assert "backend" in data, "Missing 'backend' key in health response"
        assert data["backend"] == "healthy", f"Backend status is {data.get('backend')}"
        assert "ml_service" in data, "Missing 'ml_service' key in health response"

    def test_api_get_system_readiness(self, http_client):
        """Matches frontend api.getSystemReadiness() -> GET /api/v1/ready"""
        r = http_client.get(f"{BACKEND_URL}/api/v1/ready")
        assert r.status_code == 200, f"Readiness check failed with status {r.status_code}"
        data = r.json()
        assert "backend" in data, "Missing 'backend' key in readiness response"
        assert "ml_service" in data, "Missing 'ml_service' key in readiness response"

    def test_api_recommend_fertilizer(self, http_client):
        """Matches frontend api.recommendFertilizer() -> POST /api/v1/fertilizer/recommend"""
        r = http_client.post(
            f"{BACKEND_URL}/api/v1/fertilizer/recommend",
            json=SAMPLE_RECOMMENDATION_PAYLOAD,
            headers=HEADERS,
        )
        assert r.status_code == 200, f"Recommendation request failed with status {r.status_code}: {r.text}"
        data = r.json()
        assert data.get("success") is True, "Expected success: true in recommendation response"
        assert "fertilizer" in data, "Missing 'fertilizer' prediction in response"
        assert isinstance(data["fertilizer"], str), "'fertilizer' must be a string"
        assert "model_version" in data, "Missing 'model_version' in response"
        assert "prediction_id" in data, "Missing 'prediction_id' in response"

    def test_api_get_prediction_stats(self, http_client):
        """Matches frontend api.getPredictionStats() -> GET /api/v1/predictions/stats"""
        r = http_client.get(
            f"{BACKEND_URL}/api/v1/predictions/stats",
            headers=HEADERS,
        )
        assert r.status_code == 200, f"Prediction stats failed with status {r.status_code}: {r.text}"
        data = r.json()
        assert "total_count" in data, "Missing 'total_count' in stats response"
        assert isinstance(data["total_count"], int), "'total_count' must be an integer"
        assert "daily_counts" in data, "Missing 'daily_counts' in stats response"

    def test_api_get_predictions_paginated(self, http_client):
        """Matches frontend api.getPredictions(page, perPage) -> GET /api/v1/predictions?page=1&per_page=10"""
        r = http_client.get(
            f"{BACKEND_URL}/api/v1/predictions?page=1&per_page=10",
            headers=HEADERS,
        )
        assert r.status_code == 200, f"Get predictions list failed with status {r.status_code}: {r.text}"
        data = r.json()
        assert "items" in data, "Missing 'items' array in prediction list response"
        assert "total" in data, "Missing 'total' count in prediction list response"
        assert "page" in data, "Missing 'page' number in prediction list response"
        assert "per_page" in data, "Missing 'per_page' number in prediction list response"
        assert "total_pages" in data, "Missing 'total_pages' in prediction list response"
        assert isinstance(data["items"], list), "'items' must be a list"

    def test_api_get_prediction_by_id(self, http_client):
        """Matches frontend api.getPredictionById(id) -> GET /api/v1/predictions/{id}"""
        # First fetch existing list to get a valid prediction_id
        r_list = http_client.get(
            f"{BACKEND_URL}/api/v1/predictions?page=1&per_page=1",
            headers=HEADERS,
        )
        assert r_list.status_code == 200
        items = r_list.json().get("items", [])
        if not items:
            pytest.skip("No predictions in database to query by ID")

        target_id = items[0]["prediction_id"]
        r = http_client.get(
            f"{BACKEND_URL}/api/v1/predictions/{target_id}",
            headers=HEADERS,
        )
        assert r.status_code == 200, f"Get prediction by ID failed with status {r.status_code}: {r.text}"
        detail = r.json()
        assert detail["prediction_id"] == target_id, "Returned prediction_id does not match target"
        assert "predicted_fertilizer" in detail, "Missing 'predicted_fertilizer' field"
