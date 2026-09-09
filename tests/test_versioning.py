import os
import sys
import shutil
import pytest
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "ml-service"))
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from inference.model_registry import ModelRegistry, model_registry
from inference.predictor import predictor
from database.db import log_prediction, PredictionLog, db

@pytest.fixture(autouse=True)
def setup_db():
    db.connect(reuse_if_open=True)
    db.create_tables([PredictionLog], safe=True)
    yield
    db.close()

def test_1_model_v1_loading():
    """Test 1: MODEL_VERSION=model-v1 loads model-v1 bundle."""
    os.environ["MODEL_VERSION"] = "model-v1"
    reg = ModelRegistry()
    bundle = reg.load_bundle("model-v1")
    assert bundle.model_version == "model-v1"
    assert hasattr(bundle.pipeline, "predict")
    assert hasattr(bundle.label_encoder, "classes_")

def test_2_model_v2_coexistence(tmp_path):
    """Test 2: A future model-v2 can coexist alongside model-v1 without deleting v1."""
    models_dir = Path(__file__).parent.parent / "ml-service" / "models"
    v1_dir = models_dir / "model-v1"
    v2_dir = models_dir / "model-v2"

    try:
        # Create model-v2 by copying model-v1 structure
        shutil.copytree(v1_dir, v2_dir)
        # Update v2 metadata.json
        meta_file = v2_dir / "metadata.json"
        with open(meta_file, "w") as f:
            f.write('{"model_version": "model-v2", "model_artifact": "fertilizer_xgboost_pipeline.pkl", "label_encoder": "target_label_encoder.pkl", "preprocessing_version": "preprocessing-v2", "feature_schema_version": "features-v1", "features": ["Soil_pH", "Nitrogen_Level", "Phosphorus_Level", "Potassium_Level", "Crop_Growth_Stage"]}')

        # Both v1 and v2 should exist
        assert v1_dir.exists()
        assert v2_dir.exists()

        reg = ModelRegistry()
        b1 = reg.load_bundle("model-v1")
        b2 = reg.load_bundle("model-v2")

        assert b1.model_version == "model-v1"
        assert b2.model_version == "model-v2"
        assert b2.metadata["preprocessing_version"] == "preprocessing-v2"

    finally:
        if v2_dir.exists():
            shutil.rmtree(v2_dir)

def test_3_and_test_4_environment_version_switch_and_response():
    """
    Test 3 & 4: Changing MODEL_VERSION=model-v2 loads v2 dynamically
    and prediction response contains the correct model version.
    """
    models_dir = Path(__file__).parent.parent / "ml-service" / "models"
    v1_dir = models_dir / "model-v1"
    v2_dir = models_dir / "model-v2"

    try:
        shutil.copytree(v1_dir, v2_dir)
        meta_file = v2_dir / "metadata.json"
        with open(meta_file, "w") as f:
            f.write('{"model_version": "model-v2", "model_artifact": "fertilizer_xgboost_pipeline.pkl", "label_encoder": "target_label_encoder.pkl", "preprocessing_version": "preprocessing-v2", "feature_schema_version": "features-v1", "features": ["Soil_pH", "Nitrogen_Level", "Phosphorus_Level", "Potassium_Level", "Crop_Growth_Stage"]}')

        # Switch to model-v2 via env var
        os.environ["MODEL_VERSION"] = "model-v2"
        reg = ModelRegistry()
        res = predictor.predict({
            "Soil_pH": 6.5,
            "Nitrogen_Level": 40.0,
            "Phosphorus_Level": 20.0,
            "Potassium_Level": 30.0,
            "Crop_Growth_Stage": "Vegetative"
        }, version="model-v2")

        assert res["model_version"] == "model-v2"
        assert res["preprocessing_version"] == "preprocessing-v2"

    finally:
        os.environ["MODEL_VERSION"] = "model-v1"
        if v2_dir.exists():
            shutil.rmtree(v2_dir)

def test_5_database_stores_correct_model_version():
    """Test 5: Database stores the correct model version."""
    pred_id = log_prediction(
        input_features={"Soil_pH": 6.5},
        predicted_fertilizer="Urea",
        confidence=0.95,
        model_version="model-v1",
        preprocessing_version="preprocessing-v1",
        feature_schema_version="features-v1",
        status="success"
    )

    record = PredictionLog.get_by_id(pred_id)
    assert record.model_version == "model-v1"
    assert record.predicted_fertilizer == "Urea"
    assert record.status == "success"

def test_6_rollback_v2_to_v1():
    """Test 6: Rollback from model-v2 -> model-v1 works by simply setting MODEL_VERSION=model-v1."""
    os.environ["MODEL_VERSION"] = "model-v2"
    reg = ModelRegistry()
    assert reg.get_active_version_name() == "model-v2"

    # Perform rollback
    os.environ["MODEL_VERSION"] = "model-v1"
    assert reg.get_active_version_name() == "model-v1"
    bundle = reg.load_bundle("model-v1")
    assert bundle.model_version == "model-v1"
