"""
Backend Pydantic Schemas Package.
"""

from .common import ErrorResponse, PaginatedResponse
from .recommendation import (
    CropGrowthStage,
    RecommendRequest,
    RecommendResponse,
)
from .prediction import (
    PredictionDetail,
    PredictionListResponse,
    PredictionStatsResponse,
)

__all__ = [
    "ErrorResponse",
    "PaginatedResponse",
    "CropGrowthStage",
    "RecommendRequest",
    "RecommendResponse",
    "PredictionDetail",
    "PredictionListResponse",
    "PredictionStatsResponse",
]
