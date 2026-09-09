"""
Circuit Breaker implementation for downstream ML service fault tolerance.
"""

import asyncio
import logging
import time
from enum import Enum
from typing import Optional

logger = logging.getLogger("backend.services.circuit_breaker")


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    """
    Process-local, thread-safe Circuit Breaker implementing standard state machine transitions:
      CLOSED -> (failure threshold) -> OPEN -> (cooldown) -> HALF_OPEN -> (success/failure) -> CLOSED/OPEN

    Uses asyncio.Lock for safe concurrency under async FastAPI worker execution.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        cooldown_seconds: float = 30.0,
    ):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.last_state_change: float = time.monotonic()
        self._lock = asyncio.Lock()

    async def can_execute(self) -> bool:
        """
        Check if call can be allowed based on current circuit state and cooldown window.
        """
        async with self._lock:
            if self.state == CircuitState.CLOSED:
                return True

            if self.state == CircuitState.OPEN:
                elapsed = time.monotonic() - self.last_state_change
                if elapsed >= self.cooldown_seconds:
                    logger.info(
                        "circuit_breaker_transition_half_open elapsed=%.2fs cooldown=%.2fs",
                        elapsed,
                        self.cooldown_seconds,
                    )
                    self.state = CircuitState.HALF_OPEN
                    self.last_state_change = time.monotonic()
                    return True
                return False

            # HALF_OPEN state allows a probe request
            return True

    async def record_success(self) -> None:
        """
        Record successful execution, resetting failures and transitioning HALF_OPEN -> CLOSED.
        """
        async with self._lock:
            if self.state in (CircuitState.HALF_OPEN, CircuitState.OPEN):
                logger.info(
                    "circuit_breaker_transition_closed from_state=%s failure_count_was=%d",
                    self.state.value,
                    self.failure_count,
                )
            self.failure_count = 0
            self.state = CircuitState.CLOSED
            self.last_state_change = time.monotonic()

    async def record_failure(self) -> None:
        """
        Record transient failure. Trips state to OPEN if threshold reached or if in HALF_OPEN.
        """
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.monotonic()

            if self.state == CircuitState.HALF_OPEN or self.failure_count >= self.failure_threshold:
                if self.state != CircuitState.OPEN:
                    logger.warning(
                        "circuit_breaker_transition_open from_state=%s failures=%d threshold=%d",
                        self.state.value,
                        self.failure_count,
                        self.failure_threshold,
                    )
                self.state = CircuitState.OPEN
                self.last_state_change = time.monotonic()
