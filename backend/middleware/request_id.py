"""
Request ID propagation middleware and context variable tracking.
"""

import uuid
from contextvars import ContextVar
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

HEADER_REQUEST_ID = "X-Request-ID"
request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="-")


def get_request_id() -> str:
    """Retrieve the current request ID from contextvars."""
    return request_id_ctx_var.get()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts or generates a unique request ID for correlation across
    logs, HTTP headers, DB persistence, and downstream calls.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        incoming_id = request.headers.get(HEADER_REQUEST_ID)
        if incoming_id and incoming_id.strip():
            request_id = incoming_id.strip()
        else:
            request_id = str(uuid.uuid4())

        # Store in request state for handlers
        request.state.request_id = request_id

        # Set contextvar for structured logging
        token = request_id_ctx_var.set(request_id)

        try:
            response = await call_next(request)
            response.headers[HEADER_REQUEST_ID] = request_id
            return response
        finally:
            request_id_ctx_var.reset(token)
