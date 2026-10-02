"""
Prometheus metrics middleware and endpoint for the backend API Gateway.

Exposes operational metrics at GET /metrics:
- HTTP request counts, latencies, and in-progress gauges
- ML circuit breaker state
- Prediction success/error counters
"""

import logging
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("backend.middleware.metrics")

# ---------------------------------------------------------------------------
# Application-level metrics
# ---------------------------------------------------------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests currently being processed",
    ["method", "endpoint"],
)

PREDICTION_COUNT = Counter(
    "predictions_total",
    "Total fertilizer predictions",
    ["status", "fertilizer"],
)

PREDICTION_LATENCY = Histogram(
    "prediction_latency_ms",
    "ML prediction latency in milliseconds",
    buckets=(5, 10, 25, 50, 100, 250, 500, 1000, 2500),
)

CIRCUIT_BREAKER_STATE = Gauge(
    "circuit_breaker_state",
    "Circuit breaker state: 0=CLOSED, 1=HALF_OPEN, 2=OPEN",
)

CIRCUIT_BREAKER_FAILURES = Counter(
    "circuit_breaker_failures_total",
    "Total circuit breaker recorded failures",
)


def record_prediction(status: str, fertilizer: str, latency_ms: float) -> None:
    """Record a prediction metric event."""
    PREDICTION_COUNT.labels(status=status, fertilizer=fertilizer).inc()
    PREDICTION_LATENCY.observe(latency_ms)


def record_circuit_breaker_state(state_name: str) -> None:
    """Update the circuit breaker state gauge."""
    state_map = {"CLOSED": 0, "HALF_OPEN": 1, "OPEN": 2}
    CIRCUIT_BREAKER_STATE.set(state_map.get(state_name, -1))


def record_circuit_breaker_failure() -> None:
    """Increment circuit breaker failure counter."""
    CIRCUIT_BREAKER_FAILURES.inc()


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

def _normalize_path(path: str) -> str:
    """Normalize dynamic path segments for metric label cardinality control."""
    parts = path.strip("/").split("/")
    normalized = []
    for i, part in enumerate(parts):
        # Replace UUIDs and numeric IDs with placeholder
        if len(part) == 36 and part.count("-") == 4:
            normalized.append("{id}")
        elif part.isdigit():
            normalized.append("{id}")
        else:
            normalized.append(part)
    return "/" + "/".join(normalized)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware that instruments HTTP requests with Prometheus metrics."""

    async def dispatch(self, request: Request, call_next) -> Response:
        method = request.method
        path = _normalize_path(request.url.path)

        # Skip metrics endpoint itself to avoid recursion
        if request.url.path == "/metrics":
            return await call_next(request)

        REQUESTS_IN_PROGRESS.labels(method=method, endpoint=path).inc()

        import time
        start = time.perf_counter()

        try:
            response = await call_next(request)
            duration = time.perf_counter() - start

            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status_code=response.status_code,
            ).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(duration)

            return response
        except Exception as exc:
            duration = time.perf_counter() - start
            REQUEST_COUNT.labels(method=method, endpoint=path, status_code=500).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(duration)
            raise
        finally:
            REQUESTS_IN_PROGRESS.labels(method=method, endpoint=path).dec()


# ---------------------------------------------------------------------------
# Metrics endpoint handler
# ---------------------------------------------------------------------------

async def metrics_endpoint(request: Request) -> Response:
    """Prometheus exposition endpoint returning all collected metrics."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
