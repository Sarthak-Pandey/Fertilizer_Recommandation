"""
Recommendation request and response schemas.
"""

import math
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator


class CropGrowthStage(str, Enum):
    """Allowed crop growth stages for fertilizer model prediction."""
    SOWING = "Sowing"
    VEGETATIVE = "Vegetative"
    FLOWERING = "Flowering"
    HARVEST = "Harvest"


class RecommendRequest(BaseModel):
    """Frontend request for fertilizer recommendation based on XGBoost model features."""
    Soil_pH: float = Field(..., ge=0.0, le=14.0, description="Soil pH (0-14)")
    Nitrogen_Level: float = Field(..., ge=0.0, description="Nitrogen level")
    Phosphorus_Level: float = Field(..., ge=0.0, description="Phosphorus level")
    Potassium_Level: float = Field(..., ge=0.0, description="Potassium level")
    Crop_Growth_Stage: CropGrowthStage = Field(
        ..., description="Growth stage: Sowing, Vegetative, Flowering, Harvest"
    )

    # Optional extra fields for frontend flexibility
    Soil_Type: Optional[str] = None
    Soil_Moisture: Optional[float] = None
    Temperature: Optional[float] = None
    Humidity: Optional[float] = None
    Rainfall: Optional[float] = None
    Crop_Type: Optional[str] = None

    @field_validator(
        "Soil_pH", "Nitrogen_Level", "Phosphorus_Level", "Potassium_Level",
    )
    @classmethod
    def validate_finite(cls, v: float) -> float:
        if not math.isfinite(v):
            raise ValueError("Must be a finite number")
        return v


class RecommendResponse(BaseModel):
    """Response returned after processing a recommendation request."""
    success: bool = True
    fertilizer: str
    confidence: Optional[float] = None
    model_version: str
    preprocessing_version: str
    feature_schema_version: str
    prediction_id: Optional[str] = None
    probabilities: Optional[Dict[str, float]] = None
    latency_ms: Optional[float] = Field(None, description="ML request latency in milliseconds")
