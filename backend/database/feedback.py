"""
FeedbackLog database model and CRUD operations.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional, List

import peewee

from backend.database.db import db, BaseModel

logger = logging.getLogger("backend.database.feedback")


class FeedbackLog(BaseModel):
    """
    Stores user feedback on predictions for model retraining and accuracy tracking.
    """

    feedback_id = peewee.CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    prediction_id = peewee.CharField(index=True)
    user_id = peewee.CharField(null=True, index=True)

    is_correct = peewee.BooleanField()
    actual_fertilizer = peewee.CharField(null=True)
    notes = peewee.TextField(null=True)

    created_at = peewee.DateTimeField(default=lambda: datetime.now(timezone.utc))

    class Meta:
        table_name = "feedback_logs"


def init_feedback_table():
    """Create the feedback_logs table if it doesn't exist."""
    db.create_tables([FeedbackLog], safe=True)
    logger.info("FeedbackLog table initialized")


def create_feedback(
    prediction_id: str,
    user_id: Optional[str] = None,
    is_correct: bool = True,
    actual_fertilizer: Optional[str] = None,
    notes: Optional[str] = None,
) -> FeedbackLog:
    """Create a new feedback entry."""
    feedback_id = str(uuid.uuid4())

    feedback = FeedbackLog.create(
        feedback_id=feedback_id,
        prediction_id=prediction_id,
        user_id=user_id,
        is_correct=is_correct,
        actual_fertilizer=actual_fertilizer,
        notes=notes,
    )

    logger.info(
        "feedback_created feedback_id=%s prediction_id=%s is_correct=%s",
        feedback_id,
        prediction_id,
        is_correct,
    )
    return feedback


def get_feedback_for_prediction(prediction_id: str) -> List[FeedbackLog]:
    """Get all feedback entries for a specific prediction."""
    return list(
        FeedbackLog.select()
        .where(FeedbackLog.prediction_id == prediction_id)
        .order_by(FeedbackLog.created_at.desc())
    )


def get_feedback_stats() -> dict:
    """Get aggregated feedback statistics."""
    total = FeedbackLog.select().count()
    correct = FeedbackLog.select().where(FeedbackLog.is_correct == True).count()
    incorrect = FeedbackLog.select().where(FeedbackLog.is_correct == False).count()

    return {
        "total_feedbacks": total,
        "correct_count": correct,
        "incorrect_count": incorrect,
        "accuracy_rate": round(correct / total, 4) if total > 0 else None,
    }
