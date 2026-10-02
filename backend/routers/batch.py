"""
Batch prediction router for processing multiple fertilizer recommendations in a single request.
"""

import asyncio
import logging
import time
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from backend.config import settings
from backend.database.db import log_prediction
from backend.middleware.request_id import get_request_id
from backend.schemas.recommendation import RecommendRequest, RecommendResponse
from backend.services.ml_client import MLServiceError
from backend.routers.recommendation import ml_client
from backend.utils.auth_dependency import get_optional_user

logger = logging.getLogger("backend.routers.batch")

router = APIRouter(prefix="/api/v1/fertilizer", tags=["Batch Prediction"])

MAX_BATCH_SIZE = 50


class BatchRecommendRequest(BaseModel):
    """Request containing multiple recommendation inputs."""
    items: List[RecommendRequest] = Field(
        ...,
        min_length=1,
        max_length=MAX_BATCH_SIZE,
        description=f"Array of recommendation inputs (max {MAX_BATCH_SIZE})",
    )


class BatchItemResult(BaseModel):
    """Result for a single item in a batch."""
    index: int
    success: bool
    fertilizer: Optional[str] = None
    confidence: Optional[float] = None
    model_version: Optional[str] = None
    prediction_id: Optional[str] = None
    latency_ms: Optional[float] = None
    error: Optional[str] = None


class BatchRecommendResponse(BaseModel):
    """Response for batch prediction request."""
    total: int
    succeeded: int
    failed: int
    results: List[BatchItemResult]


async def _predict_single(
    index: int,
    request: RecommendRequest,
    request_id: str,
    user_id: Optional[str],
) -> BatchItemResult:
    """Process a single prediction within a batch."""
    input_data = request.model_dump()
    crop_stage_val = (
        request.Crop_Growth_Stage.value
        if hasattr(request.Crop_Growth_Stage, "value")
        else str(request.Crop_Growth_Stage)
    )

    ml_payload = {
        "Soil_pH": request.Soil_pH,
        "Nitrogen_Level": request.Nitrogen_Level,
        "Phosphorus_Level": request.Phosphorus_Level,
        "Potassium_Level": request.Potassium_Level,
        "Crop_Growth_Stage": crop_stage_val,
    }

    item_request_id = f"{request_id}:batch-{index}"
    start_time = time.perf_counter()

    try:
        ml_result = await ml_client.predict(ml_payload)
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        fertilizer = ml_result.get("fertilizer", "Unknown")
        confidence = ml_result.get("confidence")
        model_version = ml_result.get("model_version", "unknown")

        prediction_id = log_prediction(
            input_features=input_data,
            predicted_fertilizer=fertilizer,
            confidence=confidence,
            model_version=model_version,
            preprocessing_version=ml_result.get("preprocessing_version", "preprocessing-v1"),
            feature_schema_version=ml_result.get("feature_schema_version", "features-v1"),
            request_id=item_request_id,
            user_id=user_id,
            latency_ms=latency_ms,
            status="success",
        )

        return BatchItemResult(
            index=index,
            success=True,
            fertilizer=fertilizer,
            confidence=confidence,
            model_version=model_version,
            prediction_id=prediction_id,
            latency_ms=latency_ms,
        )

    except MLServiceError as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        log_prediction(
            input_features=input_data,
            predicted_fertilizer="N/A",
            model_version="unknown",
            preprocessing_version="unknown",
            feature_schema_version="unknown",
            request_id=item_request_id,
            user_id=user_id,
            latency_ms=latency_ms,
            status="error",
            error_message=str(e),
        )
        return BatchItemResult(
            index=index,
            success=False,
            latency_ms=latency_ms,
            error=str(e),
        )

    except Exception as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return BatchItemResult(
            index=index,
            success=False,
            latency_ms=latency_ms,
            error=f"Unexpected error: {str(e)}",
        )


@router.post("/recommend/batch", response_model=BatchRecommendResponse)
async def batch_recommend(
    http_request: Request,
    payload: BatchRecommendRequest,
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Batch fertilizer recommendation endpoint.
    Processes multiple inputs concurrently via asyncio.gather().
    Maximum batch size: 50 items.
    """
    request_id = (
        getattr(http_request.state, "request_id", None)
        or get_request_id()
        or str(uuid.uuid4())
    )
    user_id = current_user.get("id") if current_user else None

    logger.info(
        "batch_recommendation_request request_id=%s batch_size=%d",
        request_id,
        len(payload.items),
    )

    # Process all items concurrently
    tasks = [
        _predict_single(i, item, request_id, user_id)
        for i, item in enumerate(payload.items)
    ]
    results = await asyncio.gather(*tasks)

    succeeded = sum(1 for r in results if r.success)
    failed = len(results) - succeeded

    logger.info(
        "batch_recommendation_completed request_id=%s total=%d succeeded=%d failed=%d",
        request_id,
        len(results),
        succeeded,
        failed,
    )

    return BatchRecommendResponse(
        total=len(results),
        succeeded=succeeded,
        failed=failed,
        results=results,
    )
