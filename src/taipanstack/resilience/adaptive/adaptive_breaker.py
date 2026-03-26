"""
Adaptive Circuit Breaker — auto-tunes failure threshold via rolling window.

Wraps a standard ``CircuitBreaker`` and dynamically adjusts its
``failure_threshold`` based on the observed error rate in a
sliding window of recent calls.
"""

from __future__ import annotations

import logging
import threading
from collections import deque
from dataclasses import dataclass
from typing import Any

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)

logger = logging.getLogger("taipanstack.resilience.adaptive.breaker")


@dataclass(frozen=True)
class AdaptiveMetrics:
    """Snapshot of adaptive circuit breaker metrics.

    Attributes:
        current_threshold: Dynamically computed failure threshold.
        success_rate: Current success rate (0.0 - 1.0).
        total_calls: Total calls in the window.
        error_count: Errors in the window.
        state: Current circuit state.

    """

    current_threshold: int
    success_rate: float
    total_calls: int
    error_count: int
    state: CircuitState


class AdaptiveCircuitBreaker:
    """Circuit breaker that auto-tunes its failure threshold.

    Maintains a rolling window of call outcomes and adjusts the
    inner ``CircuitBreaker.config.failure_threshold`` so that:

    - **High error rate** → lowers threshold (trips faster)
    - **Low error rate** → raises threshold (more tolerant)

    Args:
        name: Identifier for logging.
        window_size: Number of recent calls to track.
        min_threshold: Minimum failure threshold.
        max_threshold: Maximum failure threshold.
        target_error_rate: Desired error rate boundary.
        recovery_timeout: Seconds before half-open attempt.
        on_threshold_change: Optional callback ``(old, new)``.

    Example:
        >>> breaker = AdaptiveCircuitBreaker("api", window_size=50)
        >>> if breaker.should_allow():
        ...     try:
        ...         result = call_api()
        ...         breaker.record_success()
        ...     except Exception as e:
        ...         breaker.record_failure(e)

    """

    def __init__(
        self,
        name: str = "default",
        *,
        window_size: int = 100,
        min_threshold: int = 2,
        max_threshold: int = 20,
        target_error_rate: float = 0.1,
        recovery_timeout: float = 30.0,
        on_threshold_change: Any | None = None,
    ) -> None:
        """Initialize the adaptive circuit breaker.

        Args:
            name: Breaker name.
            window_size: Rolling window size.
            min_threshold: Minimum threshold.
            max_threshold: Maximum threshold.
            target_error_rate: Target error rate boundary.
            recovery_timeout: Seconds before half-open.
            on_threshold_change: Callback ``(old_threshold, new_threshold)``.

        """
        self.name = name
        self._window_size = window_size
        self._min_threshold = min_threshold
        self._max_threshold = max_threshold
        self._target_error_rate = target_error_rate
        self._on_threshold_change = on_threshold_change

        # Rolling window: True = success, False = failure
        self._window: deque[bool] = deque(maxlen=window_size)
        self._lock = threading.Lock()

        # Inner circuit breaker
        self._breaker = CircuitBreaker(
            name=name,
            failure_threshold=max_threshold,
            timeout=recovery_timeout,
        )

    @property
    def state(self) -> CircuitState:
        """Current circuit state."""
        return self._breaker.state

    @property
    def current_threshold(self) -> int:
        """Dynamically computed failure threshold."""
        return self._breaker.config.failure_threshold

    @property
    def inner_breaker(self) -> CircuitBreaker:
        """Access the underlying ``CircuitBreaker``."""
        return self._breaker

    def _compute_threshold(self) -> int:
        """Calculate threshold from rolling window error rate.

        Returns:
            New failure threshold clamped to [min, max].

        """
        with self._lock:
            total = len(self._window)
            if total == 0:
                return self._max_threshold

            errors = sum(1 for ok in self._window if not ok)
            error_rate = errors / total

        # High error rate → low threshold (trip faster)
        # Low error rate → high threshold (more tolerant)
        if error_rate > self._target_error_rate:
            ratio = 1.0 - min(error_rate, 1.0)
            threshold = int(
                self._min_threshold
                + ratio * (self._max_threshold - self._min_threshold)
            )
        else:
            threshold = self._max_threshold

        return max(self._min_threshold, min(threshold, self._max_threshold))

    def _update_threshold(self) -> None:
        """Recalculate and apply the adaptive threshold."""
        new_threshold = self._compute_threshold()
        old_threshold = self._breaker.config.failure_threshold

        if new_threshold != old_threshold:
            self._breaker.config.failure_threshold = new_threshold
            logger.info(
                "Adaptive breaker '%s' threshold: %d → %d",
                self.name,
                old_threshold,
                new_threshold,
            )
            if self._on_threshold_change is not None:
                self._on_threshold_change(old_threshold, new_threshold)

    def record_success(self) -> None:
        """Record a successful call."""
        with self._lock:
            self._window.append(True)
        self._breaker._record_success()
        self._update_threshold()

    def record_failure(self, exc: Exception) -> None:
        """Record a failed call.

        Args:
            exc: The exception that occurred.

        """
        with self._lock:
            self._window.append(False)
        self._breaker._record_failure(exc)
        self._update_threshold()

    def should_allow(self) -> bool:
        """Check if a call should be attempted.

        Returns:
            ``True`` if the circuit permits a call.

        """
        return self._breaker._should_attempt()

    def reset(self) -> None:
        """Reset the breaker and window."""
        with self._lock:
            self._window.clear()
        self._breaker.reset()

    @property
    def metrics(self) -> AdaptiveMetrics:
        """Snapshot of current adaptive metrics."""
        with self._lock:
            total = len(self._window)
            errors = sum(1 for ok in self._window if not ok)
            success_rate = (total - errors) / total if total > 0 else 1.0

        return AdaptiveMetrics(
            current_threshold=self.current_threshold,
            success_rate=success_rate,
            total_calls=total,
            error_count=errors,
            state=self.state,
        )
