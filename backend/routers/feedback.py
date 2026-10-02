"""
Feedback router for submitting user feedback on predictions.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.database.db import get_prediction
from backend.database.feedback import create_feedback, get_feedback_for_prediction
from backend.utils.auth_dependency import get_optional_user

logger = logging.getLogger("backend.routers.feedback")

router = APIRouter(prefix="/api/v1/predictions", tags=["Feedback"])


class FeedbackRequest(BaseModel):
    """Schema for submitting user feedback on a prediction."""
    is_correct: bool = Field(..., description="Whether the prediction was correct")
    actual_fertilizer: Optional[str] = Field(None, description="The actual fertilizer used (if different)")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes or comments")


class FeedbackResponse(BaseModel):
    """Schema for feedback response."""
    feedback_id: str
    prediction_id: str
    is_correct: bool
    actual_fertilizer: Optional[str] = None
    notes: Optional[str] = None
    created_at: str


@router.post("/{prediction_id}/feedback", response_model=FeedbackResponse, status_code=201)
async def submit_feedback(
    prediction_id: str,
    payload: FeedbackRequest,
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Submit feedback on a specific prediction.
    Records whether the prediction was correct and the actual fertilizer used.
    """
    user_id = current_user.get("id") if current_user else None

    # Verify prediction exists
    prediction = get_prediction(prediction_id, user_id=user_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    feedback = create_feedback(
        prediction_id=prediction_id,
        user_id=user_id,
        is_correct=payload.is_correct,
        actual_fertilizer=payload.actual_fertilizer,
        notes=payload.notes,
    )

    logger.info(
        "feedback_submitted prediction_id=%s is_correct=%s user_id=%s",
        prediction_id,
        payload.is_correct,
        user_id,
    )

    return FeedbackResponse(
        feedback_id=feedback.feedback_id,
        prediction_id=feedback.prediction_id,
        is_correct=feedback.is_correct,
        actual_fertilizer=feedback.actual_fertilizer,
        notes=feedback.notes,
        created_at=str(feedback.created_at),
    )


@router.get("/{prediction_id}/feedback")
async def get_feedback(
    prediction_id: str,
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """Retrieve feedback for a specific prediction."""
    user_id = current_user.get("id") if current_user else None

    prediction = get_prediction(prediction_id, user_id=user_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    feedbacks = get_feedback_for_prediction(prediction_id)

    return {
        "prediction_id": prediction_id,
        "feedbacks": [
            {
                "feedback_id": f.feedback_id,
                "is_correct": f.is_correct,
                "actual_fertilizer": f.actual_fertilizer,
                "notes": f.notes,
                "created_at": str(f.created_at),
            }
            for f in feedbacks
        ],
    }
