"""
Backend API Gateway -- FastAPI Application

The backend is the ONLY public-facing API layer.
The frontend communicates with this service, never directly with the ML service.
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from slowapi.errors import RateLimitExceeded

from backend.config import settings
from backend.database.db import close_db, init_db
from backend.database.feedback import init_feedback_table
from backend.logging_config import setup_logging
from backend.middleware.auth import APIKeyAuthMiddleware
from backend.middleware.metrics import PrometheusMiddleware, metrics_endpoint
from backend.middleware.rate_limit import limiter, rate_limit_exceeded_handler
from backend.middleware.request_id import RequestIDMiddleware, get_request_id
from backend.routers.analytics import router as analytics_router
from backend.routers.auth import router as auth_router
from backend.routers.batch import router as batch_router
from backend.routers.export import router as export_router
from backend.routers.feedback import router as feedback_router
from backend.routers.predictions import router as predictions_router
from backend.routers.recommendation import ml_client
from backend.routers.recommendation import router as recommendation_router
from backend.routers.system import router as system_router
from backend.schemas.recommendation import (
    CropGrowthStage,
    RecommendRequest,
    RecommendResponse,
)

# Configure logging according to settings
setup_logging(log_level=settings.LOG_LEVEL, log_format=settings.LOG_FORMAT)
logger = logging.getLogger("backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Backend starting... ML_SERVICE_URL=%s", settings.ML_SERVICE_URL)
    init_db()
    init_feedback_table()
    await ml_client.open()
    yield
    await ml_client.close()
    close_db()
    logger.info("Backend shut down.")


app = FastAPI(
    title="Fertilizer Recommendation Backend Gateway",
    description=(
        "Enterprise-grade API Gateway for the Fertilizer Recommendation System. "
        "Provides fertilizer prediction, prediction history auditing, analytics, "
        "batch processing, user authentication, and Prometheus observability."
    ),
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Fieldwise Engineering",
        "url": "https://github.com/Sarthak-Pandey/Fertilizer_Recommandation",
    },
    license_info={
        "name": "MIT License",
    },
    openapi_tags=[
        {"name": "Authentication", "description": "User registration, login, and session management"},
        {"name": "Recommendation", "description": "Core fertilizer recommendation endpoint"},
        {"name": "Batch Prediction", "description": "Batch processing for multiple recommendations"},
        {"name": "Predictions", "description": "Prediction history retrieval and lookup"},
        {"name": "Feedback", "description": "User feedback on prediction accuracy"},
        {"name": "Analytics", "description": "Aggregated dashboard insights and distribution data"},
        {"name": "Export", "description": "Data export in CSV and JSON formats"},
        {"name": "System", "description": "Health checks and system readiness"},
    ],
)

# Attach rate limiter state to app
app.state.limiter = limiter

# Register custom error handler for rate limiting
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Prometheus metrics middleware (innermost — closest to route handlers)
app.add_middleware(PrometheusMiddleware)

# API Key authentication middleware
app.add_middleware(APIKeyAuthMiddleware)

# Environment-restricted CORS policy (must be outer to auth middleware so preflights pass)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Request ID correlation middleware (outermost for incoming requests)
app.add_middleware(RequestIDMiddleware)

# Register API Routers
app.include_router(auth_router)
app.include_router(recommendation_router)
app.include_router(batch_router)
app.include_router(predictions_router)
app.include_router(export_router)
app.include_router(feedback_router)
app.include_router(analytics_router)
app.include_router(system_router)

# Prometheus metrics exposition endpoint (public, no auth required)
app.add_route("/metrics", metrics_endpoint, methods=["GET"])


@app.get("/", include_in_schema=False)
async def serve_index_html():
    """Serve the API Gateway index or health info."""
    import os
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html")
    return JSONResponse(
        content={
            "status": "online",
            "service": "Fertilizer Recommendation Backend Gateway",
            "version": "1.0.0",
            "docs_url": "/docs",
            "health_url": "/api/v1/health",
            "metrics_url": "/metrics",
        }
    )



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", None) or get_request_id()
    logger.error(
        "unhandled_backend_error request_id=%s exc_type=%s exc_msg=%s",
        req_id,
        type(exc).__name__,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"},
        headers={"X-Request-ID": req_id},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
