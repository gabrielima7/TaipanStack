"""Tests for AdaptiveRetry."""

from taipanstack.resilience.adaptive.adaptive_retry import (
    AdaptiveRetry,
    RetryMetrics,
)
from taipanstack.resilience.retry import RetryConfig


class TestAdaptiveRetry:
    """Tests for the adaptive retry strategy."""

    def test_adaptive_retry_fallback_delay_without_data(self) -> None:
        """Uses exponential backoff when no outcomes recorded."""
        ar = AdaptiveRetry(min_delay=0.1, max_delay=10.0)
        d1 = ar.get_delay(1)
        d2 = ar.get_delay(2)
        assert d1 >= 0.1
        assert d2 > d1

    def test_adaptive_retry_learned_delay_from_successes(
        self,
    ) -> None:
        """Returns median of successful delays when data available."""
        ar = AdaptiveRetry(min_delay=0.1, max_delay=10.0)
        ar.record_outcome(attempt=1, success=True, elapsed=0.5)
        ar.record_outcome(attempt=1, success=True, elapsed=0.7)
        ar.record_outcome(attempt=1, success=True, elapsed=0.3)

        delay = ar.get_delay(1)
        assert 0.3 <= delay <= 0.7

    def test_adaptive_retry_failure_does_not_affect_delay(
        self,
    ) -> None:
        """Failures are not used for delay computation."""
        ar = AdaptiveRetry(min_delay=0.1, max_delay=10.0)
        ar.record_outcome(attempt=1, success=False, elapsed=5.0)
        ar.record_outcome(attempt=1, success=True, elapsed=0.5)

        delay = ar.get_delay(1)
        assert delay == 0.5

    def test_adaptive_retry_delay_clamped_to_bounds(self) -> None:
        """Delay is clamped to [min_delay, max_delay]."""
        ar = AdaptiveRetry(min_delay=1.0, max_delay=5.0)
        ar.record_outcome(attempt=1, success=True, elapsed=0.01)
        assert ar.get_delay(1) >= 1.0

        ar2 = AdaptiveRetry(min_delay=0.1, max_delay=2.0)
        ar2.record_outcome(attempt=1, success=True, elapsed=100.0)
        assert ar2.get_delay(1) <= 2.0

    def test_adaptive_retry_to_retry_config(self) -> None:
        """Converts to standard RetryConfig."""
        ar = AdaptiveRetry(min_delay=0.1, max_delay=30.0, max_attempts=5)
        ar.record_outcome(attempt=1, success=True, elapsed=0.5)

        config = ar.to_retry_config()
        assert isinstance(config, RetryConfig)
        assert config.max_attempts == 5
        assert config.max_delay == 30.0
        assert not config.jitter

    def test_adaptive_retry_metrics_snapshot(self) -> None:
        """Metrics reports correct values."""
        ar = AdaptiveRetry()
        ar.record_outcome(attempt=1, success=True, elapsed=1.0)
        ar.record_outcome(attempt=1, success=True, elapsed=2.0)
        ar.record_outcome(attempt=2, success=False, elapsed=3.0)

        m = ar.metrics
        assert isinstance(m, RetryMetrics)
        assert m.total_outcomes == 3
        assert m.success_rate > 0.6
        assert m.avg_delay == 2.0

    def test_adaptive_retry_empty_metrics(self) -> None:
        """Metrics with no data returns defaults."""
        ar = AdaptiveRetry()
        m = ar.metrics
        assert m.total_outcomes == 0
        assert m.success_rate == 1.0
        assert m.avg_delay == 0.0

    def test_adaptive_retry_per_attempt_isolation(self) -> None:
        """Delays are tracked per attempt level."""
        ar = AdaptiveRetry(min_delay=0.1, max_delay=100.0)
        ar.record_outcome(attempt=1, success=True, elapsed=1.0)
        ar.record_outcome(attempt=2, success=True, elapsed=5.0)

        assert ar.get_delay(1) == 1.0
        assert ar.get_delay(2) == 5.0

    def test_adaptive_retry_max_delay_exponential_fallback(
        self,
    ) -> None:
        """Exponential fallback respects max_delay."""
        ar = AdaptiveRetry(min_delay=1.0, max_delay=5.0)
        delay = ar.get_delay(10)
        assert delay <= 5.0
