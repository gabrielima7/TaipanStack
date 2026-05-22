"""
Adaptive Circuit Breaker — auto-tunes failure threshold via rolling window.

Unlike standard Circuit Breakers that use static absolute failure counts,
the AdaptiveCircuitBreaker opens its circuit ONLY when the error rate
exceeds a target percentage in a rolling window of recent calls AND a
minimum throughput of requests has been met.
"""

from __future__ import annotations

import logging
import math
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import TypeVar

from taipanstack.core.result import Ok, Result
from taipanstack.resilience.circuit_breaker import CircuitState

logger = logging.getLogger("taipanstack.resilience.adaptive.breaker")

T = TypeVar("T")


@dataclass(frozen=True)
class AdaptiveMetrics:
    """Snapshot of adaptive circuit breaker metrics.

    Attributes:
        success_rate: Current success rate (0.0 - 1.0).
        error_rate: Current error rate (0.0 - 1.0).
        total_calls: Total calls in the window.
        error_count: Errors in the window.
        state: Current circuit state.

    """

    success_rate: float
    error_rate: float
    total_calls: int
    error_count: int
    state: CircuitState


class AdaptiveCircuitBreaker:
    """Circuit breaker that opens based on an error rate percentage.

    Maintains a rolling window of call outcomes. The circuit trips to OPEN if:
    1. The `window_size` history has at least `min_throughput` events.
    2. The error rate (errors / total) > `target_error_rate`.

    Once OPEN, it waits `recovery_timeout` seconds before transitioning
    to HALF_OPEN. In HALF_OPEN, if a request succeeds, it CLOSES and
    clears the window. If it fails, it returns to OPEN.

    Args:
        name: Identifier for logging.
        window_size: Number of recent calls to track.
        min_throughput: Minimum requests before considering error rate.
        target_error_rate: Desired error rate boundary (0.0 - 1.0).
        recovery_timeout: Seconds before attempting half-open recovery.

    """

    def __init__(
        self,
        name: str = "default",
        *,
        window_size: int = 100,
        min_throughput: int = 10,
        target_error_rate: float = 0.5,
        recovery_timeout: float = 30.0,
    ) -> None:
        """Initialize the adaptive circuit breaker."""
        self.name = name
        if min_throughput < 1:
            raise ValueError("min_throughput must be at least 1")
        self._min_throughput = min_throughput
        self._target_error_rate = target_error_rate
        if not math.isfinite(recovery_timeout) or recovery_timeout < 0:
            raise ValueError("recovery_timeout must be a finite non-negative number")
        self._recovery_timeout = recovery_timeout

        # Rolling window: True = success, False = failure
        self._window: deque[bool] = deque(maxlen=window_size)
        self._state = CircuitState.CLOSED
        self._last_opened_at: float = 0.0
        self._lock = threading.Lock()

    def _calculate_elapsed_time(self, now: float) -> float:
        """Calculate elapsed time since the circuit opened."""
        last_opened = self._last_opened_at
        if not isinstance(last_opened, (int, float)) or not math.isfinite(last_opened):
            return self._recovery_timeout

        elapsed = now - last_opened
        return self._recovery_timeout if elapsed < 0 else elapsed

    def _check_half_open_transition(self) -> None:
        """Evaluate if an OPEN circuit should transition to HALF_OPEN."""
        now = time.monotonic()
        elapsed = self._calculate_elapsed_time(now)

        if math.isfinite(now) and elapsed >= self._recovery_timeout:
            self._state = CircuitState.HALF_OPEN
            logger.info("Adaptive breaker '%s' entering HALF_OPEN state", self.name)

    @property
    def state(self) -> CircuitState:
        """Current circuit state. May evaluate timeouts and switch to HALF_OPEN."""
        with self._lock:
            if self._state == CircuitState.OPEN:
                self._check_half_open_transition()
            return self._state

    def _calculate_error_rate(self, total: int) -> float:
        """Calculate the current error rate in the window."""
        if total <= 0:
            return 0.0
        errors = sum(1 for ok in self._window if not ok)
        return errors / total

    def _get_safe_target_rate(self) -> float:
        """Safely retrieve the target error rate."""
        target_rate = self._target_error_rate
        if not isinstance(target_rate, (int, float)) or not math.isfinite(target_rate):
            return -1.0  # Fail closed
        return float(target_rate)

    def _transition_to_open(self, error_rate: float, target_rate: float) -> None:
        """Transition the circuit to the OPEN state."""
        self._state = CircuitState.OPEN
        self._last_opened_at = time.monotonic()

        log_target = target_rate if target_rate >= 0 else 0.0
        logger.warning(
            "Adaptive breaker '%s' OPENED. Error rate %.2f > %.2f",
            self.name,
            error_rate,
            log_target,
        )

    def _evaluate_trip(self) -> None:
        """Evaluate if the circuit should trip open.

        MUST BE CALLED UNDER LOCK.
        """
        if self._state != CircuitState.CLOSED:
            return

        total = len(self._window)
        if total < self._min_throughput:
            return

        error_rate = self._calculate_error_rate(total)
        target_rate = self._get_safe_target_rate()

        if error_rate > target_rate:
            self._transition_to_open(error_rate, target_rate)

    def record_success(self) -> None:
        """Record a successful call."""
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                # Full recovery on success
                self._state = CircuitState.CLOSED
                self._window.clear()
                logger.info(
                    "Adaptive breaker '%s' CLOSED after successful half-open recovery.",
                    self.name,
                )

            self._window.append(True)
            self._evaluate_trip()

    def record_failure(self, _exc: Exception) -> None:
        """Record a failed call.

        Args:
            _exc: The exception that occurred.

        """
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                # Return to open immediately on failure
                self._state = CircuitState.OPEN
                self._last_opened_at = time.monotonic()
                logger.warning(
                    "Adaptive breaker '%s' RETURNED to OPEN after half-open failure.",
                    self.name,
                )

            self._window.append(False)
            self._evaluate_trip()

    def evaluate_result(self, result: Result[T, Exception]) -> Result[T, Exception]:
        """Evaluate a Result and record success or failure.

        Args:
            result: A ``Result`` to evaluate.

        Returns:
            The original Result.

        """
        if isinstance(result, Ok):
            self.record_success()
        else:
            self.record_failure(result.err_value)
        return result

    def should_allow(self) -> bool:
        """Check if a call should be attempted.

        Returns:
            ``True`` if the circuit permits a call.

        """
        return self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN)

    def reset(self) -> None:
        """Reset the breaker and window."""
        with self._lock:
            self._window.clear()
            self._state = CircuitState.CLOSED
            self._last_opened_at = 0.0

    @property
    def metrics(self) -> AdaptiveMetrics:
        """Snapshot of current adaptive metrics."""
        with self._lock:
            total = len(self._window)
            errors = sum(1 for ok in self._window if not ok)
            error_rate = errors / total if total > 0 else 0.0
            success_rate = 1.0 - error_rate
            state_val = self._state

        return AdaptiveMetrics(
            success_rate=success_rate,
            error_rate=error_rate,
            total_calls=total,
            error_count=errors,
            state=state_val,
        )
