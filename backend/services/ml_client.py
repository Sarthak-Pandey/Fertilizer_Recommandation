"""
ML Client -- Centralized HTTP communication with the ML Inference Service.

All backend-to-ML HTTP calls go through this single module using persistent HTTP connection pooling,
exponential backoff retries for transient failures, and circuit breaker fault tolerance.
"""

import asyncio
import logging
from typing import Any, Optional
import httpx

from backend.config import settings
from backend.services.circuit_breaker import CircuitBreaker

logger = logging.getLogger("backend.ml_client")


class MLServiceError(Exception):
    """Raised when the ML service returns an error or is unreachable."""
    def __init__(self, message: str, status_code: int = 503):
        super().__init__(message)
        self.status_code = status_code


class MLClient:
    """
    HTTP client for the ML Inference Service using a shared, persistent connection pool,
    exponential retry policy, and circuit breaker.
    """
    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        max_retries: Optional[int] = None,
        retry_base_delay: Optional[float] = None,
        retry_max_delay: Optional[float] = None,
        circuit_breaker: Optional[CircuitBreaker] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries if max_retries is not None else settings.ML_MAX_RETRIES
        self.retry_base_delay = (
            retry_base_delay if retry_base_delay is not None else settings.ML_RETRY_BASE_DELAY
        )
        self.retry_max_delay = (
            retry_max_delay if retry_max_delay is not None else settings.ML_RETRY_MAX_DELAY
        )
        self.circuit_breaker = (
            circuit_breaker
            if circuit_breaker is not None
            else CircuitBreaker(
                failure_threshold=settings.ML_CIRCUIT_FAILURE_THRESHOLD,
                cooldown_seconds=settings.ML_CIRCUIT_COOLDOWN_SECONDS,
            )
        )
        self._client: Optional[httpx.AsyncClient] = None

    async def open(self) -> None:
        """Initialize the underlying persistent HTTP AsyncClient connection pool."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
            logger.info("ml_client_connection_pool_opened base_url=%s", self.base_url)

    async def close(self) -> None:
        """Close the underlying HTTP AsyncClient connection pool."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
            logger.info("ml_client_connection_pool_closed")

    def _get_client(self) -> httpx.AsyncClient:
        """Get or lazily instantiate the shared AsyncClient."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    async def predict(self, input_data: dict[str, Any]) -> dict:
        """
        Send a prediction request to the ML service with retries and circuit breaker protection.

        Returns the parsed JSON response dict.
        Raises MLServiceError on failure.
        """
        url = f"{self.base_url}/predict"
        logger.info("ml_request_started url=%s", url)

        if not await self.circuit_breaker.can_execute():
            logger.warning("ml_circuit_breaker_open url=%s", url)
            raise MLServiceError(
                "ML service circuit breaker is OPEN (service unavailable)",
                status_code=503,
            )

        last_error: Optional[MLServiceError] = None

        for attempt in range(1, self.max_retries + 1):
            client = self._get_client()

            try:
                response = await client.post("/predict", json=input_data)
            except httpx.ConnectError as e:
                logger.error("ml_service_unreachable url=%s error=%s attempt=%d", url, e, attempt)
                last_error = MLServiceError("ML service is unavailable", status_code=503)
            except httpx.TimeoutException as e:
                logger.error("ml_request_timeout url=%s timeout=%s attempt=%d", url, self.timeout, attempt)
                last_error = MLServiceError(
                    f"ML service request timed out after {self.timeout}s",
                    status_code=504,
                )
            except httpx.HTTPError as e:
                logger.error("ml_request_http_error url=%s error=%s attempt=%d", url, e, attempt)
                last_error = MLServiceError(f"ML service HTTP error: {e}", status_code=502)
            else:
                if response.status_code == 422:
                    detail = response.json().get("detail", "Validation error")
                    logger.warning("ml_validation_error detail=%s", detail)
                    # Validation error is client input error: non-retryable, not a circuit failure
                    raise MLServiceError(f"Invalid input: {detail}", status_code=400)

                if response.status_code == 503:
                    logger.error("ml_model_not_loaded attempt=%d", attempt)
                    last_error = MLServiceError("ML model not loaded", status_code=503)
                elif response.status_code != 200:
                    body = response.text[:200]
                    logger.error(
                        "ml_unexpected_status status=%d body=%s attempt=%d",
                        response.status_code,
                        body,
                        attempt,
                    )
                    last_error = MLServiceError(
                        f"ML service returned status {response.status_code}",
                        status_code=502,
                    )
                else:
                    try:
                        result = response.json()
                    except Exception as e:
                        logger.error("ml_invalid_json_response error=%s attempt=%d", e, attempt)
                        last_error = MLServiceError(
                            "Invalid JSON response from ML service", status_code=502
                        )
                    else:
                        if isinstance(result, dict) and "error" in result and result.get("success") is False:
                            error_msg = result.get("error", "Unknown ML error")
                            logger.error("ml_prediction_failed error=%s attempt=%d", error_msg, attempt)
                            last_error = MLServiceError(f"ML prediction failed: {error_msg}", status_code=500)
                        else:
                            await self.circuit_breaker.record_success()
                            logger.info(
                                "ml_request_completed model_version=%s attempt=%d",
                                result.get("model_version") if isinstance(result, dict) else "unknown",
                                attempt,
                            )
                            return result

            # Retry transient failure if attempts remain
            if attempt < self.max_retries:
                delay = min(self.retry_max_delay, self.retry_base_delay * (2 ** (attempt - 1)))
                logger.warning(
                    "ml_retry_attempt attempt=%d max_retries=%d status=%s delay_s=%.2f",
                    attempt,
                    self.max_retries,
                    getattr(last_error, "status_code", "unknown"),
                    delay,
                )
                await asyncio.sleep(delay)

        # Exhausted retries on transient errors -> record circuit failure
        await self.circuit_breaker.record_failure()
        raise last_error or MLServiceError("ML service request failed after retries", status_code=503)

    async def health(self) -> dict:
        """Check ML service health using connection pool."""
        try:
            client = self._get_client()
            response = await client.get("/health", timeout=5.0)
            return response.json()
        except Exception as e:
            logger.error("ml_health_check_failed error=%s", e)
            return {"status": "unreachable", "error": str(e)}

    async def ready(self) -> dict:
        """Check ML service readiness using connection pool."""
        try:
            client = self._get_client()
            response = await client.get("/ready", timeout=5.0)
            return response.json()
        except Exception as e:
            logger.error("ml_ready_check_failed error=%s", e)
            return {"status": "unreachable", "model_loaded": False, "error": str(e)}
