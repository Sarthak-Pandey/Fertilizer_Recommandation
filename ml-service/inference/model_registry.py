import os
import json
import joblib
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class ModelBundle:
    model_version: str
    pipeline: Any
    label_encoder: Any
    metadata: Dict[str, Any]

class ModelRegistry:
    def __init__(self, base_models_dir: Optional[str] = None):
        if base_models_dir is None:
            base_models_dir = os.getenv("MODELS_DIR", os.path.join(os.path.dirname(__file__), "..", "models"))
        self.base_models_dir = Path(base_models_dir).resolve()
        self._cache: Dict[str, ModelBundle] = {}

    def get_active_version_name(self) -> str:
        # Priority: Environment variable MODEL_VERSION -> registry.json -> default "model-v1"
        env_version = os.getenv("MODEL_VERSION")
        if env_version:
            return env_version
        
        registry_file = self.base_models_dir / "registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, "r") as f:
                    reg = json.load(f)
                    if "production" in reg:
                        return reg["production"]
            except Exception:
                pass
        return "model-v1"

    def load_bundle(self, version: Optional[str] = None) -> ModelBundle:
        if version is None:
            version = self.get_active_version_name()

        if version in self._cache:
            return self._cache[version]

        version_dir = self.base_models_dir / version
        if not version_dir.exists():
            raise FileNotFoundError(f"Model version directory not found: {version_dir}")

        metadata_path = version_dir / "metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        model_artifact_name = metadata.get("model_artifact", "fertilizer_xgboost_pipeline.pkl")
        encoder_artifact_name = metadata.get("label_encoder", "target_label_encoder.pkl")

        pipeline_path = version_dir / model_artifact_name
        encoder_path = version_dir / encoder_artifact_name

        if not pipeline_path.exists():
            raise FileNotFoundError(f"Pipeline artifact missing: {pipeline_path}")
        if not encoder_path.exists():
            raise FileNotFoundError(f"Label encoder artifact missing: {encoder_path}")

        # Load artifacts
        pipeline = joblib.load(pipeline_path)
        label_encoder = joblib.load(encoder_path)

        # Validate bundle integrity
        self._validate_bundle(version, pipeline, label_encoder, metadata)

        bundle = ModelBundle(
            model_version=version,
            pipeline=pipeline,
            label_encoder=label_encoder,
            metadata=metadata
        )
        self._cache[version] = bundle
        return bundle

    def _validate_bundle(self, version: str, pipeline: Any, label_encoder: Any, metadata: Dict[str, Any]):
        if not hasattr(pipeline, "predict"):
            raise ValueError(f"Pipeline in {version} does not support predict()")
        
        if not hasattr(label_encoder, "classes_"):
            raise ValueError(f"Label encoder in {version} missing classes_ attribute")

        if metadata.get("model_version") and metadata.get("model_version") != version:
            raise ValueError(f"Metadata version mismatch: {metadata.get('model_version')} vs directory {version}")

model_registry = ModelRegistry()
