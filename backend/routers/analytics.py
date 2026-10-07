"""
Analytics router providing aggregated dashboard insights and distribution data.
"""

import logging
from typing import Dict, List, Optional

import peewee
from fastapi import APIRouter, Depends, Query

from backend.database.db import PredictionLog, DATABASE_URL
from backend.utils.auth_dependency import get_optional_user

logger = logging.getLogger("backend.routers.analytics")

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


@router.get("/summary")
async def analytics_summary(
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Aggregated analytics summary: total predictions, success/error rate,
    average confidence, and average latency.
    """
    user_id = current_user.get("id") if current_user else None
    active_filter = (PredictionLog.is_deleted == False) | (PredictionLog.is_deleted.is_null(True))

    base = PredictionLog.select().where(active_filter)
    if user_id:
        base = base.where(PredictionLog.user_id == user_id)

    total = base.count()

    success_count = base.where(PredictionLog.status == "success").count()
    error_count = base.where(PredictionLog.status == "error").count()

    avg_conf_q = (
        PredictionLog.select(peewee.fn.AVG(PredictionLog.confidence))
        .where(
            (PredictionLog.status == "success")
            & (PredictionLog.confidence.is_null(False))
            & active_filter
        )
    )
    if user_id:
        avg_conf_q = avg_conf_q.where(PredictionLog.user_id == user_id)
    avg_conf = avg_conf_q.scalar()

    avg_lat_q = (
        PredictionLog.select(peewee.fn.AVG(PredictionLog.latency_ms))
        .where(
            (PredictionLog.status == "success")
            & (PredictionLog.latency_ms.is_null(False))
            & active_filter
        )
    )
    if user_id:
        avg_lat_q = avg_lat_q.where(PredictionLog.user_id == user_id)
    avg_lat = avg_lat_q.scalar()

    return {
        "total_predictions": total,
        "success_count": success_count,
        "error_count": error_count,
        "success_rate": round(success_count / total, 4) if total > 0 else None,
        "average_confidence": round(float(avg_conf), 4) if avg_conf is not None else None,
        "average_latency_ms": round(float(avg_lat), 2) if avg_lat is not None else None,
    }


@router.get("/distribution")
async def analytics_distribution(
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Prediction count per fertilizer type (distribution chart data).
    """
    user_id = current_user.get("id") if current_user else None
    active_filter = (PredictionLog.is_deleted == False) | (PredictionLog.is_deleted.is_null(True))

    query = (
        PredictionLog.select(
            PredictionLog.predicted_fertilizer,
            peewee.fn.COUNT(PredictionLog.prediction_id).alias("count"),
        )
        .where((PredictionLog.status == "success") & active_filter)
    )
    if user_id:
        query = query.where(PredictionLog.user_id == user_id)

    query = query.group_by(PredictionLog.predicted_fertilizer).order_by(
        peewee.SQL("count").desc()
    )

    distribution: Dict[str, int] = {}
    for row in query:
        distribution[row.predicted_fertilizer] = int(row.count)

    return {"distribution": distribution}


@router.get("/timeline")
async def analytics_timeline(
    granularity: str = Query("daily", pattern="^(daily|weekly)$", description="Granularity: daily or weekly"),
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Predictions over time (daily or weekly) for trend visualization.
    """
    user_id = current_user.get("id") if current_user else None
    active_filter = (PredictionLog.is_deleted == False) | (PredictionLog.is_deleted.is_null(True))

    if DATABASE_URL.startswith("postgresql"):
        if granularity == "weekly":
            date_expr = peewee.fn.to_char(
                peewee.fn.date_trunc("week", PredictionLog.created_at), "YYYY-MM-DD"
            )
        else:
            date_expr = peewee.fn.to_char(PredictionLog.created_at, "YYYY-MM-DD")
    else:
        if granularity == "weekly":
            # SQLite: group by start of ISO week
            date_expr = peewee.fn.strftime(
                "%Y-%m-%d", PredictionLog.created_at, "weekday 0", "-6 days"
            )
        else:
            date_expr = peewee.fn.strftime("%Y-%m-%d", PredictionLog.created_at)

    query = PredictionLog.select(
        date_expr.alias("period"),
        peewee.fn.COUNT(PredictionLog.prediction_id).alias("count"),
    ).where(active_filter)
    if user_id:
        query = query.where(PredictionLog.user_id == user_id)

    query = query.group_by(date_expr).order_by(date_expr.asc())

    timeline: Dict[str, int] = {}
    for row in query:
        period = getattr(row, "period", None)
        if period:
            timeline[str(period)] = int(row.count)

    return {"granularity": granularity, "timeline": timeline}


@router.get("/model-performance")
async def analytics_model_performance(
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Average confidence and prediction count per model version.
    """
    user_id = current_user.get("id") if current_user else None
    active_filter = (PredictionLog.is_deleted == False) | (PredictionLog.is_deleted.is_null(True))

    query = (
        PredictionLog.select(
            PredictionLog.model_version,
            peewee.fn.COUNT(PredictionLog.prediction_id).alias("count"),
            peewee.fn.AVG(PredictionLog.confidence).alias("avg_confidence"),
            peewee.fn.AVG(PredictionLog.latency_ms).alias("avg_latency_ms"),
        )
        .where((PredictionLog.status == "success") & active_filter)
    )
    if user_id:
        query = query.where(PredictionLog.user_id == user_id)

    query = query.group_by(PredictionLog.model_version).order_by(
        peewee.SQL("count").desc()
    )

    models: List[dict] = []
    for row in query:
        models.append({
            "model_version": row.model_version,
            "prediction_count": int(row.count),
            "average_confidence": round(float(row.avg_confidence), 4) if row.avg_confidence else None,
            "average_latency_ms": round(float(row.avg_latency_ms), 2) if row.avg_latency_ms else None,
        })

    return {"models": models}
