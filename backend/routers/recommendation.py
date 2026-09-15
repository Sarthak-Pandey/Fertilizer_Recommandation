"""
Recommendation router handling fertilizer recommendation endpoints.
"""

import logging
import time
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request

from backend.config import settings
from backend.database.db import log_prediction
from backend.middleware.request_id import get_request_id
from backend.schemas.recommendation import RecommendRequest, RecommendResponse
from backend.services.ml_client import MLClient, MLServiceError
from backend.utils.auth_dependency import get_optional_user

logger = logging.getLogger("backend.routers.recommendation")

router = APIRouter(prefix="/api/v1/fertilizer", tags=["Recommendation"])

# Shared MLClient instance
ml_client = MLClient(
    base_url=settings.ML_SERVICE_URL,
    timeout=settings.ML_REQUEST_TIMEOUT,
)


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(
    http_request: Request,
    request: RecommendRequest,
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Fertilizer recommendation endpoint.
    Flow: Frontend -> Backend -> ML Service -> DB Persist -> Response
    """
    request_id = (
        getattr(http_request.state, "request_id", None)
        or get_request_id()
        or str(uuid.uuid4())
    )
    input_data = request.model_dump()

    # Convert Crop_Growth_Stage enum to string value for ML payload
    crop_stage_val = (
        request.Crop_Growth_Stage.value
        if hasattr(request.Crop_Growth_Stage, "value")
        else str(request.Crop_Growth_Stage)
    )

    logger.info("recommendation_request request_id=%s", request_id)

    # ML service expects exact features
    ml_payload = {
        "Soil_pH": request.Soil_pH,
        "Nitrogen_Level": request.Nitrogen_Level,
        "Phosphorus_Level": request.Phosphorus_Level,
        "Potassium_Level": request.Potassium_Level,
        "Crop_Growth_Stage": crop_stage_val,
    }

    user_id = current_user.get("id") if current_user else None

    start_time = time.perf_counter()
    try:
        ml_result = await ml_client.predict(ml_payload)
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    except MLServiceError as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.error(
            "recommendation_failed request_id=%s error=%s status=%d latency_ms=%.2f",
            request_id, str(e), e.status_code, latency_ms,
        )
        log_prediction(
            input_features=input_data,
            predicted_fertilizer="N/A",
            model_version="unknown",
            preprocessing_version="unknown",
            feature_schema_version="unknown",
            request_id=request_id,
            user_id=user_id,
            latency_ms=latency_ms,
            status="error",
            error_message=str(e),
        )
        raise HTTPException(status_code=e.status_code, detail=str(e))

    # Extract results
    fertilizer = ml_result.get("fertilizer", "Unknown")
    confidence = ml_result.get("confidence")
    model_version = ml_result.get("model_version", "unknown")
    preprocessing_version = ml_result.get("preprocessing_version", "preprocessing-v1")
    feature_schema_version = ml_result.get("feature_schema_version", "features-v1")
    probabilities = ml_result.get("probabilities")

    # Persist prediction in DB
    prediction_id = log_prediction(
        input_features=input_data,
        predicted_fertilizer=fertilizer,
        confidence=confidence,
        model_version=model_version,
        preprocessing_version=preprocessing_version,
        feature_schema_version=feature_schema_version,
        request_id=request_id,
        user_id=user_id,
        latency_ms=latency_ms,
        status="success",
    )

    return RecommendResponse(
        success=True,
        fertilizer=fertilizer,
        confidence=confidence,
        model_version=model_version,
        preprocessing_version=preprocessing_version,
        feature_schema_version=feature_schema_version,
        prediction_id=prediction_id,
        probabilities=probabilities,
        latency_ms=latency_ms,
    )
