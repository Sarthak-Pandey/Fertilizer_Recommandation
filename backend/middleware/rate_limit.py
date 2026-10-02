"""
Rate limiting middleware using slowapi.

Enforces per-IP and per-API-key request rate limits.
Returns HTTP 429 Too Many Requests with Retry-After header when exceeded.
"""

import logging
from typing import Optional

from fastapi import Request, Response
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from backend.config import settings

logger = logging.getLogger("backend.middleware.rate_limit")


def _key_func(request: Request) -> str:
    """
    Extract rate-limit key from request.
    Priority: X-API-Key header > Authorization Bearer user > client IP.
    """
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"apikey:{api_key}"

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        # Use first 16 chars of token as key to avoid storing full tokens
        token_prefix = auth_header[7:23]
        return f"bearer:{token_prefix}"

    return get_remote_address(request)


# Create the limiter instance
limiter = Limiter(
    key_func=_key_func,
    default_limits=[settings.RATE_LIMIT_DEFAULT],
    storage_uri="memory://",
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Custom handler for rate limit exceeded errors."""
    retry_after = exc.detail.split("per")[-1].strip() if exc.detail else "60"

    logger.warning(
        "rate_limit_exceeded client=%s path=%s detail=%s",
        _key_func(request),
        request.url.path,
        exc.detail,
    )

    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": "Too many requests. Please slow down.",
            "detail": str(exc.detail),
        },
        headers={"Retry-After": retry_after},
    )
