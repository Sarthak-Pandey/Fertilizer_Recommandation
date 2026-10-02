"""
Backend Routers Package.
"""

from .recommendation import router as recommendation_router
from .system import router as system_router
from .predictions import router as predictions_router
from .auth import router as auth_router
from .analytics import router as analytics_router
from .batch import router as batch_router
from .export import router as export_router
from .feedback import router as feedback_router

__all__ = [
    "recommendation_router",
    "system_router",
    "predictions_router",
    "auth_router",
    "analytics_router",
    "batch_router",
    "export_router",
    "feedback_router",
]
