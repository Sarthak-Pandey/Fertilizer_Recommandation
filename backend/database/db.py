"""
Database -- PredictionLog model and connection management.

Uses peewee ORM with SQLite (local) / PostgreSQL (Docker).
Stores all version identifiers for every prediction for full traceability.
"""

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

import peewee

logger = logging.getLogger("backend.database")

# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./predictions.db")

if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.replace("sqlite:///", "").replace("sqlite://", "")
    if db_path.startswith("./"):
        db_path = db_path[2:]
    db = peewee.SqliteDatabase(db_path)
elif DATABASE_URL.startswith("postgresql"):
    from playhouse.db_url import connect as pw_connect
    db = pw_connect(DATABASE_URL)
else:
    db = peewee.SqliteDatabase("predictions.db")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class BaseModel(peewee.Model):
    class Meta:
        database = db


class PredictionLog(BaseModel):
    """
    Stores every prediction for traceability and auditing.

    Six months later we can answer: "Which model generated this prediction?"
    """

    prediction_id = peewee.CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = peewee.CharField(null=True, index=True)
    user_id = peewee.CharField(null=True, index=True)

    # Input features stored as JSON
    input_features = peewee.TextField()

    # Prediction results
    predicted_fertilizer = peewee.CharField()
    gate_decision = peewee.CharField(null=True, default="N/A")
    specialist_used = peewee.CharField(null=True)
    confidence = peewee.FloatField(null=True)

    # Version tracking -- critical for traceability
    model_version = peewee.CharField(index=True)
    preprocessing_version = peewee.CharField()
    feature_schema_version = peewee.CharField()

    # Operational
    latency_ms = peewee.FloatField(null=True)
    status = peewee.CharField(default="success")  # success | error
    error_message = peewee.TextField(null=True)

    created_at = peewee.DateTimeField(default=lambda: datetime.now(timezone.utc))

    class Meta:
        table_name = "prediction_logs"


# ---------------------------------------------------------------------------
# Init / Migrate
# ---------------------------------------------------------------------------

def init_db():
    """Create tables and execute migrations."""
    db.connect(reuse_if_open=True)
    db.create_tables([PredictionLog], safe=True)
    from backend.database.migrations.runner import run_migrations
    run_migrations(db)
    logger.info("Database initialized with migrations applied: %s", DATABASE_URL)


def close_db():
    """Close the database connection."""
    if not db.is_closed():
        db.close()


def log_prediction(
    input_features: dict,
    predicted_fertilizer: str,
    model_version: str,
    preprocessing_version: str,
    feature_schema_version: str,
    confidence: Optional[float] = None,
    gate_decision: Optional[str] = "N/A",
    specialist_used: Optional[str] = None,
    latency_ms: Optional[float] = None,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    status: str = "success",
    error_message: Optional[str] = None,
) -> str:
    """
    Log a prediction to the database. Returns the prediction_id.
    """
    prediction_id = str(uuid.uuid4())

    try:
        PredictionLog.create(
            prediction_id=prediction_id,
            request_id=request_id,
            user_id=user_id,
            input_features=json.dumps(input_features),
            predicted_fertilizer=predicted_fertilizer,
            gate_decision=gate_decision,
            specialist_used=specialist_used,
            confidence=confidence,
            model_version=model_version,
            preprocessing_version=preprocessing_version,
            feature_schema_version=feature_schema_version,
            latency_ms=latency_ms,
            status=status,
            error_message=error_message,
        )
        logger.info(
            "prediction_logged id=%s model_version=%s fertilizer=%s",
            prediction_id, model_version, predicted_fertilizer,
        )
    except Exception as e:
        logger.error("prediction_log_failed error=%s", e)
        # Database failure should not crash the API
        return prediction_id

    return prediction_id


# ---------------------------------------------------------------------------
# Query / Read layer functions
# ---------------------------------------------------------------------------

def get_prediction(prediction_id: str, user_id: Optional[str] = None) -> Optional[PredictionLog]:
    """Retrieve a single PredictionLog entry by ID. Optionally verifies user_id ownership."""
    query = PredictionLog.select().where(PredictionLog.prediction_id == prediction_id)
    if user_id:
        query = query.where(PredictionLog.user_id == user_id)
    return query.first()


def count_predictions(filters: Optional[dict] = None, user_id: Optional[str] = None) -> int:
    """Return total count of prediction logs, with optional filtering and user scoping."""
    query = PredictionLog.select()
    if user_id:
        query = query.where(PredictionLog.user_id == user_id)
    if filters and "status" in filters:
        query = query.where(PredictionLog.status == filters["status"])
    return query.count()


def list_predictions(
    page: int = 1,
    per_page: int = 20,
    filters: Optional[dict] = None,
    user_id: Optional[str] = None,
) -> list[PredictionLog]:
    """
    Return a paginated list of PredictionLog records ordered by newest first.
    Pagination and user filtering are applied directly at the database query level.
    """
    page = max(1, page)
    per_page = max(1, min(100, per_page))
    offset = (page - 1) * per_page

    query = PredictionLog.select()
    if user_id:
        query = query.where(PredictionLog.user_id == user_id)
    if filters and "status" in filters:
        query = query.where(PredictionLog.status == filters["status"])

    return list(query.order_by(PredictionLog.created_at.desc()).offset(offset).limit(per_page))


def get_prediction_stats(user_id: Optional[str] = None) -> dict:
    """
    Compute aggregated prediction statistics using database-level aggregation.
    Optionally scoped to a specific user_id.
    """
    base_query = PredictionLog.select()
    if user_id:
        base_query = base_query.where(PredictionLog.user_id == user_id)

    total_count = base_query.count()

    # Average confidence score for successful predictions
    avg_query = PredictionLog.select(peewee.fn.AVG(PredictionLog.confidence)).where(
        (PredictionLog.status == "success") & (PredictionLog.confidence.is_null(False))
    )
    if user_id:
        avg_query = avg_query.where(PredictionLog.user_id == user_id)
    avg_val = avg_query.scalar()
    average_confidence = round(float(avg_val), 4) if avg_val is not None else None

    # Most frequent fertilizer
    most_freq_query = (
        PredictionLog.select(
            PredictionLog.predicted_fertilizer,
            peewee.fn.COUNT(PredictionLog.prediction_id).alias("cnt"),
        )
        .where(PredictionLog.status == "success")
    )
    if user_id:
        most_freq_query = most_freq_query.where(PredictionLog.user_id == user_id)

    most_freq_query = (
        most_freq_query.group_by(PredictionLog.predicted_fertilizer)
        .order_by(peewee.SQL("cnt").desc())
        .limit(1)
    )
    most_freq_rows = list(most_freq_query)
    most_frequent_fertilizer = (
        most_freq_rows[0].predicted_fertilizer if most_freq_rows else None
    )

    # Daily prediction counts using database-compatible date aggregation
    if DATABASE_URL.startswith("postgresql"):
        date_expr = peewee.fn.to_char(PredictionLog.created_at, "YYYY-MM-DD")
    else:
        date_expr = peewee.fn.strftime("%Y-%m-%d", PredictionLog.created_at)

    daily_query = PredictionLog.select(
        date_expr.alias("day"),
        peewee.fn.COUNT(PredictionLog.prediction_id).alias("cnt"),
    )
    if user_id:
        daily_query = daily_query.where(PredictionLog.user_id == user_id)

    daily_query = daily_query.group_by(date_expr).order_by(date_expr.asc())

    daily_counts = {}
    for row in daily_query:
        day_str = getattr(row, "day", None)
        if day_str:
            daily_counts[str(day_str)] = int(getattr(row, "cnt", 0))

    return {
        "total_count": total_count,
        "average_confidence": average_confidence,
        "most_frequent_fertilizer": most_frequent_fertilizer,
        "daily_counts": daily_counts,
    }

