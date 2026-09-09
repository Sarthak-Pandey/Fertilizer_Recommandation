"""
Prediction history and stats schemas.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field

from .common import PaginatedResponse


class PredictionDetail(BaseModel):
    """Detailed model representing a single logged prediction."""
    prediction_id: str
    request_id: Optional[str] = None
    input_features: Dict[str, Any] = Field(..., description="JSON input features")
    predicted_fertilizer: str
    gate_decision: Optional[str] = "N/A"
    specialist_used: Optional[str] = None
    confidence: Optional[float] = None
    model_version: str
    preprocessing_version: str
    feature_schema_version: str
    latency_ms: Optional[float] = None
    status: str = "success"
    error_message: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionListResponse(PaginatedResponse[PredictionDetail]):
    """Paginated list of prediction history details."""
    pass


class PredictionStatsResponse(BaseModel):
    """Aggregated prediction statistics."""
    total_count: int = Field(0, description="Total number of prediction requests")
    average_confidence: Optional[float] = Field(None, description="Average confidence score of successful predictions")
    most_frequent_fertilizer: Optional[str] = Field(None, description="Most commonly recommended fertilizer")
    daily_counts: Dict[str, int] = Field(default_factory=dict, description="Daily prediction counts keyed by YYYY-MM-DD")
