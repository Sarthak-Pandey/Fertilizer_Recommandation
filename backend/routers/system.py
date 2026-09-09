"""
System router handling health and readiness checks.
"""

from fastapi import APIRouter
from backend.routers.recommendation import ml_client

router = APIRouter(prefix="/api/v1", tags=["System"])


@router.get("/health")
async def backend_health():
    """Health check endpoint checking backend and ML service health."""
    ml_health = await ml_client.health()
    return {
        "backend": "healthy",
        "ml_service": ml_health,
    }


@router.get("/ready")
async def backend_ready():
    """Readiness check endpoint checking backend and ML service readiness."""
    ml_ready = await ml_client.ready()
    return {
        "backend": "ready",
        "ml_service": ml_ready,
    }
