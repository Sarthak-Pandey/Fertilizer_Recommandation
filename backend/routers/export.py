"""
Data export router for downloading prediction history in CSV or JSON format.
"""

import csv
import io
import json
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from starlette.responses import StreamingResponse

from backend.database.db import PredictionLog
from backend.utils.auth_dependency import get_optional_user

logger = logging.getLogger("backend.routers.export")

router = APIRouter(prefix="/api/v1/predictions", tags=["Export"])


@router.get("/export")
async def export_predictions(
    format: str = Query("csv", pattern="^(csv|json)$", description="Export format: csv or json"),
    date_from: Optional[str] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Export prediction history as CSV or JSON file download.
    Supports optional date range filtering.
    """
    user_id = current_user.get("id") if current_user else None

    query = PredictionLog.select().where(
        (PredictionLog.status == "success")
        & ((PredictionLog.is_deleted == False) | (PredictionLog.is_deleted.is_null(True)))
    )

    if user_id:
        query = query.where(PredictionLog.user_id == user_id)

    if date_from:
        try:
            from_dt = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.where(PredictionLog.created_at >= from_dt)
        except ValueError:
            pass

    if date_to:
        try:
            to_dt = datetime.strptime(date_to, "%Y-%m-%d")
            # Include the entire end date
            to_dt = to_dt.replace(hour=23, minute=59, second=59)
            query = query.where(PredictionLog.created_at <= to_dt)
        except ValueError:
            pass

    query = query.order_by(PredictionLog.created_at.desc()).limit(10000)
    records = list(query)

    logger.info("export_requested format=%s records=%d user_id=%s", format, len(records), user_id)

    if format == "json":
        return _export_json(records)
    else:
        return _export_csv(records)


def _record_to_dict(record: PredictionLog) -> dict:
    """Convert a PredictionLog record to a flat dictionary."""
    input_features = record.input_features
    if isinstance(input_features, str):
        try:
            input_features = json.loads(input_features)
        except Exception:
            input_features = {"raw": input_features}

    return {
        "prediction_id": record.prediction_id,
        "request_id": record.request_id or "",
        "predicted_fertilizer": record.predicted_fertilizer,
        "confidence": record.confidence,
        "model_version": record.model_version,
        "latency_ms": record.latency_ms,
        "status": record.status,
        "soil_ph": input_features.get("Soil_pH", ""),
        "nitrogen_level": input_features.get("Nitrogen_Level", ""),
        "phosphorus_level": input_features.get("Phosphorus_Level", ""),
        "potassium_level": input_features.get("Potassium_Level", ""),
        "crop_growth_stage": input_features.get("Crop_Growth_Stage", ""),
        "created_at": str(record.created_at) if record.created_at else "",
    }


def _export_csv(records: list) -> StreamingResponse:
    """Generate CSV streaming response."""
    output = io.StringIO()
    fieldnames = [
        "prediction_id", "request_id", "predicted_fertilizer", "confidence",
        "model_version", "latency_ms", "status", "soil_ph", "nitrogen_level",
        "phosphorus_level", "potassium_level", "crop_growth_stage", "created_at",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for record in records:
        writer.writerow(_record_to_dict(record))

    output.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"predictions_export_{timestamp}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


def _export_json(records: list) -> StreamingResponse:
    """Generate JSON streaming response."""
    data = [_record_to_dict(record) for record in records]
    content = json.dumps({"predictions": data, "total": len(data)}, indent=2)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"predictions_export_{timestamp}.json"

    return StreamingResponse(
        iter([content]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
