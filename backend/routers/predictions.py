"""
Predictions router handling prediction history read endpoints.
"""

import json
from fastapi import APIRouter, HTTPException, Query

from backend.database.db import (
    PredictionLog,
    count_predictions,
    get_prediction,
    get_prediction_stats,
    list_predictions,
)
from backend.schemas.prediction import (
    PredictionDetail,
    PredictionListResponse,
    PredictionStatsResponse,
)
from backend.utils.pagination import calculate_total_pages, normalize_pagination_params

router = APIRouter(prefix="/api/v1/predictions", tags=["Predictions"])


def _to_prediction_detail(log: PredictionLog) -> PredictionDetail:
    """Convert a PredictionLog ORM model to a PredictionDetail Pydantic schema."""
    if isinstance(log.input_features, str):
        try:
            input_features_dict = json.loads(log.input_features)
        except Exception:
            input_features_dict = {"raw": log.input_features}
    else:
        input_features_dict = log.input_features or {}

    return PredictionDetail(
        prediction_id=log.prediction_id,
        request_id=log.request_id,
        input_features=input_features_dict,
        predicted_fertilizer=log.predicted_fertilizer,
        gate_decision=log.gate_decision,
        specialist_used=log.specialist_used,
        confidence=log.confidence,
        model_version=log.model_version,
        preprocessing_version=log.preprocessing_version,
        feature_schema_version=log.feature_schema_version,
        latency_ms=log.latency_ms,
        status=log.status,
        error_message=log.error_message,
        created_at=log.created_at,
    )


@router.get("", response_model=PredictionListResponse)
@router.get("/", response_model=PredictionListResponse, include_in_schema=False)
async def get_predictions(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page (1-100)"),
):
    """
    Retrieve paginated prediction history, ordered by newest first.
    Pagination is applied at the database level.
    """
    norm_page, norm_per_page = normalize_pagination_params(page, per_page)
    logs = list_predictions(page=norm_page, per_page=norm_per_page)
    total = count_predictions()
    total_pages = calculate_total_pages(total, norm_per_page)

    items = [_to_prediction_detail(log) for log in logs]

    return PredictionListResponse(
        items=items,
        total=total,
        page=norm_page,
        per_page=norm_per_page,
        total_pages=total_pages,
    )


@router.get("/stats", response_model=PredictionStatsResponse)
async def get_stats():
    """
    Retrieve aggregated prediction statistics.
    Includes total predictions count, average confidence score, most frequent fertilizer, and daily counts.
    """
    stats = get_prediction_stats()
    return PredictionStatsResponse(
        total_count=stats.get("total_count", 0),
        average_confidence=stats.get("average_confidence"),
        most_frequent_fertilizer=stats.get("most_frequent_fertilizer"),
        daily_counts=stats.get("daily_counts", {}),
    )


@router.get("/{prediction_id}", response_model=PredictionDetail)
async def get_single_prediction(prediction_id: str):
    """
    Retrieve a single prediction by prediction_id.
    Returns HTTP 404 if prediction is not found.
    """
    log = get_prediction(prediction_id)
    if not log:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return _to_prediction_detail(log)
