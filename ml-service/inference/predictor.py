import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from inference.model_registry import model_registry, ModelBundle

class FertilizerPredictor:
    def __init__(self, registry=model_registry):
        self.registry = registry

    def predict(self, input_features: Dict[str, Any], version: Optional[str] = None) -> Dict[str, Any]:
        bundle: ModelBundle = self.registry.load_bundle(version)

        # Expected features order from metadata or pipeline
        expected_features = bundle.metadata.get("features", [
            "Soil_pH", "Nitrogen_Level", "Phosphorus_Level", "Potassium_Level", "Crop_Growth_Stage"
        ])

        # Validate presence of features
        missing = [f for f in expected_features if f not in input_features]
        if missing:
            raise ValueError(f"Missing required features: {missing}")

        # Construct DataFrame in exact feature order
        input_data = {f: [input_features[f]] for f in expected_features}
        df_input = pd.DataFrame(input_data)

        # 1. Pipeline preprocessing + model inference
        raw_pred = bundle.pipeline.predict(df_input)
        pred_class_idx = int(raw_pred[0])

        # 2. Decode label
        decoded_label = str(bundle.label_encoder.inverse_transform([pred_class_idx])[0])

        # 3. Calculate confidence and probabilities if supported
        confidence = None
        proba_dict = None
        if hasattr(bundle.pipeline, "predict_proba"):
            try:
                probas = bundle.pipeline.predict_proba(df_input)[0]
                classes = bundle.label_encoder.classes_
                proba_dict = {str(c): float(p) for c, p in zip(classes, probas)}
                confidence = float(np.max(probas))
            except Exception:
                pass

        return {
            "fertilizer": decoded_label,
            "confidence": round(confidence, 4) if confidence is not None else None,
            "model_version": bundle.model_version,
            "preprocessing_version": bundle.metadata.get("preprocessing_version", "preprocessing-v1"),
            "feature_schema_version": bundle.metadata.get("feature_schema_version", "features-v1"),
            "probabilities": proba_dict
        }

predictor = FertilizerPredictor()
