from pydantic import BaseModel, Field
from typing import Dict, Optional, Literal

class FertilizerPredictionRequest(BaseModel):
    Soil_pH: float = Field(..., ge=0.0, le=14.0, description="Soil pH value (0-14)")
    Nitrogen_Level: float = Field(..., ge=0.0, description="Nitrogen content (mg/kg or kg/ha)")
    Phosphorus_Level: float = Field(..., ge=0.0, description="Phosphorus content (mg/kg or kg/ha)")
    Potassium_Level: float = Field(..., ge=0.0, description="Potassium content (mg/kg or kg/ha)")
    Crop_Growth_Stage: str = Field(..., description="Crop growth stage: Sowing, Vegetative, Flowering, or Harvest")

    class Config:
        json_schema_extra = {
            "example": {
                "Soil_pH": 6.5,
                "Nitrogen_Level": 40.0,
                "Phosphorus_Level": 20.0,
                "Potassium_Level": 30.0,
                "Crop_Growth_Stage": "Vegetative"
            }
        }

class FertilizerPredictionResponse(BaseModel):
    fertilizer: str = Field(..., description="Recommended fertilizer label")
    confidence: Optional[float] = Field(None, description="Prediction probability confidence score (0-1)")
    model_version: str = Field(..., description="Version of the model used for prediction")
    preprocessing_version: str = Field("preprocessing-v1", description="Preprocessing version")
    feature_schema_version: str = Field("features-v1", description="Feature schema version")
    probabilities: Optional[Dict[str, float]] = Field(None, description="Class probabilities mapping")
