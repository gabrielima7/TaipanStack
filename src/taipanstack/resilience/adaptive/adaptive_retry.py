"""
Adaptive Retry — learns optimal backoff from runtime outcomes.

Tracks recent retry outcomes in a rolling window and computes
the best delay for each attempt level, favouring delays that
historically led to successful retries.
"""

from __future__ import annotations

import logging
import statistics
import threading
from collections import defaultdict, deque
from dataclasses import dataclass

from taipanstack.resilience.retry import RetryConfig

logger = logging.getLogger("taipanstack.resilience.adaptive.retry")


@dataclass(frozen=True)
class RetryMetrics:
    """Snapshot of adaptive retry metrics.

    Attributes:
        success_rate: Overall success rate (0.0 - 1.0).
        avg_delay: Average delay across all successful retries.
        p95_delay: 95th percentile delay.
        total_outcomes: Total tracked outcomes.

    """

    success_rate: float
    avg_delay: float
    p95_delay: float
    total_outcomes: int


@dataclass(frozen=True)
class _Outcome:
    """Record of a single retry outcome."""

    attempt: int
    success: bool
    elapsed: float


class AdaptiveRetry:
    """Retry strategy that learns optimal delays from outcomes.

    Maintains per-attempt-level statistics and returns the delay
    that historically led to successful retries at that attempt
    level.

    Args:
        min_delay: Minimum delay in seconds.
        max_delay: Maximum delay in seconds.
        window_size: Number of recent outcomes to track.
        max_attempts: Default max attempts for ``to_retry_config()``.

    Example:
        >>> ar = AdaptiveRetry(min_delay=0.1, max_delay=30.0)
        >>> ar.record_outcome(attempt=1, success=True, elapsed=0.5)
        >>> delay = ar.get_delay(attempt=1)

    """

    def __init__(
        self,
        *,
        min_delay: float = 0.1,
        max_delay: float = 60.0,
        window_size: int = 50,
        max_attempts: int = 3,
    ) -> None:
        """Initialize the adaptive retry.

        Args:
            min_delay: Minimum delay.
            max_delay: Maximum delay.
            window_size: Rolling window size.
            max_attempts: Default max attempts.

        """
        self._min_delay = min_delay
        self._max_delay = max_delay
        self._max_attempts = max_attempts
        self._lock = threading.Lock()

        # Per-attempt deque of outcomes
        self._outcomes: deque[_Outcome] = deque(maxlen=window_size)
        # Per-attempt successful delays
        self._success_delays: dict[int, deque[float]] = defaultdict(
            lambda: deque(maxlen=window_size)
        )

    def record_outcome(
        self,
        attempt: int,
        success: bool,
        elapsed: float,
    ) -> None:
        """Record a retry outcome.

        Args:
            attempt: Attempt number (1-indexed).
            success: Whether the attempt succeeded.
            elapsed: Time elapsed before this attempt was made.

        """
        outcome = _Outcome(attempt=attempt, success=success, elapsed=elapsed)
        with self._lock:
            self._outcomes.append(outcome)
            if success:
                self._success_delays[attempt].append(elapsed)

    def get_delay(self, attempt: int) -> float:
        """Get the learned optimal delay for this attempt level.

        If there is historical data for this attempt level, returns
        the median of successful delays. Otherwise uses exponential
        backoff with the configured bounds.

        Args:
            attempt: Attempt number (1-indexed).

        Returns:
            Delay in seconds.

        """
        with self._lock:
            delays = list(self._success_delays.get(attempt, []))

        if delays:
            # Use median of successful delays as the optimal delay
            learned = statistics.median(delays)
            return max(self._min_delay, min(learned, self._max_delay))

        # Fallback: exponential backoff
        fallback_delay = self._min_delay * (2.0 ** (attempt - 1))
        return max(self._min_delay, min(fallback_delay, self._max_delay))

    def to_retry_config(self) -> RetryConfig:
        """Export current state as a standard ``RetryConfig``.

        Uses the learned initial delay (attempt=1) if available.

        Returns:
            A ``RetryConfig`` snapshot.

        """
        initial = self.get_delay(1)
        return RetryConfig(
            max_attempts=self._max_attempts,
            initial_delay=initial,
            max_delay=self._max_delay,
            jitter=False,
        )
