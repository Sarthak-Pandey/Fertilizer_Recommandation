"""
Backend Routers Package.
"""

from .recommendation import router as recommendation_router
from .system import router as system_router
from .predictions import router as predictions_router

__all__ = [
    "recommendation_router",
    "system_router",
    "predictions_router",
]
