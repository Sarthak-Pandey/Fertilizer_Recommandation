"""
Phase 1 Test Suite — Verifies Core Completeness & Architectural Refactoring.

Tests:
- CropGrowthStage enum validation (valid values & HTTP 422 rejections)
- Pagination utilities & API pagination
- Database read layer functions (get_prediction, list_predictions, count_predictions, get_prediction_stats)
- Prediction history endpoints (GET /api/v1/predictions, GET /api/v1/predictions/stats, GET /api/v1/predictions/{id})
- Latency tracking in recommendation flow
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch

root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi.testclient import TestClient
from backend import main
from backend.config import settings
from backend.main import app
from backend.database.db import (
    db,
    PredictionLog,
    log_prediction,
    get_prediction,
    list_predictions,
    count_predictions,
    get_prediction_stats,
)
from backend.schemas.recommendation import CropGrowthStage, RecommendRequest
from backend.utils.pagination import (
    normalize_pagination_params,
    calculate_offset,
    calculate_total_pages,
)

client = TestClient(app, headers={"X-API-Key": settings.API_KEY})


@pytest.fixture(autouse=True)
def setup_db():
    db.connect(reuse_if_open=True)
    db.create_tables([PredictionLog], safe=True)
    # Clear existing rows for deterministic test state
    PredictionLog.delete().execute()
    yield
    db.close()


# ---------------------------------------------------------------------------
# 1. CropGrowthStage Enum Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("valid_stage", ["Sowing", "Vegetative", "Flowering", "Harvest"])
def test_crop_growth_stage_enum_valid(valid_stage):
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": valid_stage,
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
        response = client.post("/api/v1/fertilizer/recommend", json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True


@pytest.mark.parametrize("invalid_stage", ["Unknown", "flowering", "SOWING", "", "Harvesting", "123"])
def test_crop_growth_stage_enum_invalid(invalid_stage):
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": invalid_stage,
    }
    response = client.post("/api/v1/fertilizer/recommend", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# 2. Pagination Helper Utility Tests
# ---------------------------------------------------------------------------

def test_pagination_utilities():
    # Normalization
    assert normalize_pagination_params(0, 150) == (1, 100)
    assert normalize_pagination_params(2, 20) == (2, 20)
    assert normalize_pagination_params(-5, -10) == (1, 1)

    # Offset
    assert calculate_offset(1, 20) == 0
    assert calculate_offset(2, 20) == 20
    assert calculate_offset(3, 10) == 20

    # Total pages ceiling division
    assert calculate_total_pages(125, 20) == 7
    assert calculate_total_pages(120, 20) == 6
    assert calculate_total_pages(0, 20) == 0
    assert calculate_total_pages(1, 20) == 1


# ---------------------------------------------------------------------------
# 3. Database Read Layer Unit Tests
# ---------------------------------------------------------------------------

def test_db_read_layer_functions():
    # Populate test predictions
    id1 = log_prediction(
        input_features={"Soil_pH": 6.5, "Crop_Growth_Stage": "Vegetative"},
        predicted_fertilizer="Urea",
        confidence=0.90,
        model_version="v1",
        preprocessing_version="v1",
        feature_schema_version="v1",
        latency_ms=12.5,
        status="success",
    )
    id2 = log_prediction(
        input_features={"Soil_pH": 7.0, "Crop_Growth_Stage": "Flowering"},
        predicted_fertilizer="DAP",
        confidence=0.80,
        model_version="v1",
        preprocessing_version="v1",
        feature_schema_version="v1",
        latency_ms=15.0,
        status="success",
    )

    # Test get_prediction
    pred1 = get_prediction(id1)
    assert pred1 is not None
    assert pred1.predicted_fertilizer == "Urea"
    assert pred1.confidence == 0.90

    missing = get_prediction("non-existent-uuid")
    assert missing is None

    # Test count_predictions & list_predictions
    assert count_predictions() == 2
    logs = list_predictions(page=1, per_page=10)
    assert len(logs) == 2

    # Test get_prediction_stats
    stats = get_prediction_stats()
    assert stats["total_count"] == 2
    assert stats["average_confidence"] == 0.85
    assert stats["most_frequent_fertilizer"] in ["Urea", "DAP"]
    assert len(stats["daily_counts"]) >= 1


# ---------------------------------------------------------------------------
# 4. Prediction API Endpoint Tests
# ---------------------------------------------------------------------------

def test_get_predictions_empty_db():
    response = client.get("/api/v1/predictions")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["per_page"] == 20
    assert data["total_pages"] == 0


def test_get_predictions_paginated():
    # Insert 5 test predictions
    for i in range(5):
        log_prediction(
            input_features={"Soil_pH": 6.0 + (i * 0.1), "Crop_Growth_Stage": "Vegetative"},
            predicted_fertilizer="Urea" if i % 2 == 0 else "DAP",
            confidence=0.85 + (i * 0.02),
            model_version="v1",
            preprocessing_version="v1",
            feature_schema_version="v1",
            status="success",
        )

    # Request page 1 with per_page 2
    res_page1 = client.get("/api/v1/predictions?page=1&per_page=2")
    assert res_page1.status_code == 200
    d1 = res_page1.json()
    assert len(d1["items"]) == 2
    assert d1["total"] == 5
    assert d1["page"] == 1
    assert d1["per_page"] == 2
    assert d1["total_pages"] == 3

    # Request page 3 with per_page 2 (1 item left)
    res_page3 = client.get("/api/v1/predictions?page=3&per_page=2")
    assert res_page3.status_code == 200
    d3 = res_page3.json()
    assert len(d3["items"]) == 1


def test_get_predictions_invalid_query_params():
    res_page_zero = client.get("/api/v1/predictions?page=0")
    assert res_page_zero.status_code == 422

    res_per_page_large = client.get("/api/v1/predictions?per_page=101")
    assert res_per_page_large.status_code == 422


def test_get_prediction_by_id_success():
    pred_id = log_prediction(
        input_features={"Soil_pH": 6.5, "Crop_Growth_Stage": "Sowing"},
        predicted_fertilizer="MOP",
        confidence=0.92,
        model_version="model-v1",
        preprocessing_version="preprocessing-v1",
        feature_schema_version="features-v1",
        status="success",
    )

    response = client.get(f"/api/v1/predictions/{pred_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["prediction_id"] == pred_id
    assert data["predicted_fertilizer"] == "MOP"
    assert data["confidence"] == 0.92
    assert data["input_features"]["Soil_pH"] == 6.5


def test_get_prediction_by_id_404_not_found():
    response = client.get("/api/v1/predictions/unknown-id-12345")
    assert response.status_code == 404
    assert response.json()["detail"] == "Prediction not found"


def test_get_prediction_stats_endpoint():
    log_prediction(
        input_features={"Soil_pH": 6.5},
        predicted_fertilizer="Urea",
        confidence=0.90,
        model_version="v1",
        preprocessing_version="v1",
        feature_schema_version="v1",
        status="success",
    )
    log_prediction(
        input_features={"Soil_pH": 6.8},
        predicted_fertilizer="Urea",
        confidence=0.94,
        model_version="v1",
        preprocessing_version="v1",
        feature_schema_version="v1",
        status="success",
    )

    response = client.get("/api/v1/predictions/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 2
    assert data["average_confidence"] == 0.92
    assert data["most_frequent_fertilizer"] == "Urea"
    assert isinstance(data["daily_counts"], dict)


# ---------------------------------------------------------------------------
# 5. Latency Measurement End-to-End Test
# ---------------------------------------------------------------------------

def test_recommendation_latency_tracking():
    payload = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative",
    }
    mock_ml_response = {
        "fertilizer": "Urea",
        "confidence": 0.98,
        "model_version": "model-v1",
        "preprocessing_version": "preprocessing-v1",
        "feature_schema_version": "features-v1",
    }

    with patch.object(main.ml_client, "predict", new_callable=AsyncMock) as mock_predict:
        mock_predict.return_value = mock_ml_response
        response = client.post("/api/v1/fertilizer/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert "latency_ms" in data
        assert data["latency_ms"] is not None
        assert isinstance(data["latency_ms"], float)
        assert data["latency_ms"] >= 0.0

        # Verify DB log latency
        log_entry = PredictionLog.get_or_none(PredictionLog.prediction_id == data["prediction_id"])
        assert log_entry is not None
        assert log_entry.latency_ms == data["latency_ms"]
