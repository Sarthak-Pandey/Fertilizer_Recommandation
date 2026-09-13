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

from backend.config import settings
from backend.database.db import close_db, init_db
from backend.logging_config import setup_logging
from backend.middleware.auth import APIKeyAuthMiddleware
from backend.middleware.request_id import RequestIDMiddleware, get_request_id
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
    await ml_client.open()
    yield
    await ml_client.close()
    close_db()
    logger.info("Backend shut down.")


app = FastAPI(
    title="Fertilizer Recommendation Backend Gateway",
    version="1.0.0",
    lifespan=lifespan,
)

# Environment-restricted CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication middleware
app.add_middleware(APIKeyAuthMiddleware)

# Register Request ID correlation middleware (outermost for incoming requests)
app.add_middleware(RequestIDMiddleware)

# Register API Routers
app.include_router(recommendation_router)
app.include_router(predictions_router)
app.include_router(system_router)


@app.get("/", response_class=FileResponse, include_in_schema=False)
async def serve_index_html():
    """Serve the interactive web application dashboard."""
    return FileResponse("templates/index.html")



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
