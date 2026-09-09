import sys
import importlib.util
import joblib
import pandas as pd
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Load ml-service main.py with unique module name
ml_service_main_path = Path(__file__).parent.parent / "ml-service" / "main.py"
spec = importlib.util.spec_from_file_location("ml_service_main_direct", ml_service_main_path)
ml_service_main = importlib.util.module_from_spec(spec)
sys.modules["ml_service_main_direct"] = ml_service_main

ml_service_dir = str(Path(__file__).parent.parent / "ml-service")
if ml_service_dir not in sys.path:
    sys.path.insert(0, ml_service_dir)

spec.loader.exec_module(ml_service_main)

app = ml_service_main.app
client = TestClient(app)

def test_direct_model_vs_api_prediction():
    """
    Mandatory Test: Verifies that direct inference on .pkl artifacts
    produces the EXACT same prediction and label decoding as the API endpoint.
    """
    # 1. Load original artifacts directly
    pipeline_path = Path(__file__).parent.parent / "ml-service" / "models" / "model-v1" / "fertilizer_xgboost_pipeline.pkl"
    encoder_path = Path(__file__).parent.parent / "ml-service" / "models" / "model-v1" / "target_label_encoder.pkl"

    direct_pipeline = joblib.load(pipeline_path)
    direct_encoder = joblib.load(encoder_path)

    # Sample Input A
    input_dict = {
        "Soil_pH": 6.5,
        "Nitrogen_Level": 40.0,
        "Phosphorus_Level": 20.0,
        "Potassium_Level": 30.0,
        "Crop_Growth_Stage": "Vegetative"
    }

    # 2. Direct Inference
    df_input = pd.DataFrame([{
        "Soil_pH": input_dict["Soil_pH"],
        "Nitrogen_Level": input_dict["Nitrogen_Level"],
        "Phosphorus_Level": input_dict["Phosphorus_Level"],
        "Potassium_Level": input_dict["Potassium_Level"],
        "Crop_Growth_Stage": input_dict["Crop_Growth_Stage"]
    }])

    direct_raw_pred = direct_pipeline.predict(df_input)
    direct_decoded = direct_encoder.inverse_transform(direct_raw_pred)[0]

    # 3. API Inference
    with TestClient(app) as test_client:
        response = test_client.post("/predict", json=input_dict)
        assert response.status_code == 200
        api_data = response.json()
        api_decoded = api_data["fertilizer"]

    # 4. Compare
    print(f"Direct Prediction: {direct_decoded}")
    print(f"API Prediction:    {api_decoded}")

    assert direct_decoded == api_decoded, f"Mismatch: Direct='{direct_decoded}' vs API='{api_decoded}'"
