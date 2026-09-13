"""
API Key Authentication middleware for protecting sensitive endpoints.
"""

import logging
from typing import Set

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from backend.config import settings
from backend.middleware.request_id import get_request_id

logger = logging.getLogger("backend.middleware.auth")

HEADER_API_KEY = "X-API-Key"

# Paths exempt from authentication requirements
PUBLIC_PATHS: Set[str] = {
    "",
    "/",
    "/api/v1/health",
    "/api/v1/ready",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico",
}


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware enforcing X-API-Key header authentication on protected routes.
    Bypasses public system health & documentation endpoints.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # HTTP OPTIONS preflight requests must bypass API key auth for CORS
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path.rstrip("/")
        if path in PUBLIC_PATHS or path.startswith("/docs") or path.startswith("/openapi"):
            return await call_next(request)

        provided_key = request.headers.get(HEADER_API_KEY)
        req_id = getattr(request.state, "request_id", None) or get_request_id()

        # Validate key
        if not provided_key or provided_key != settings.API_KEY:
            logger.warning(
                "authentication_failed request_id=%s path=%s reason=%s",
                req_id,
                path,
                "missing_key" if not provided_key else "invalid_key",
            )
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "error": "Unauthorized: Invalid or missing API key",
                },
                headers={"X-Request-ID": req_id},
            )

        return await call_next(request)
