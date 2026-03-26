"""Tests for AdaptiveCircuitBreaker."""

from taipanstack.resilience.adaptive.adaptive_breaker import (
    AdaptiveCircuitBreaker,
    AdaptiveMetrics,
)
from taipanstack.resilience.circuit_breaker import CircuitState


class TestAdaptiveCircuitBreaker:
    """Tests for the adaptive circuit breaker."""

    def test_initial_state_closed(self) -> None:
        """Starts in CLOSED state with max threshold."""
        ab = AdaptiveCircuitBreaker("test", max_threshold=10)
        assert ab.state == CircuitState.CLOSED
        assert ab.current_threshold == 10
        assert ab.should_allow()

    def test_record_success(self) -> None:
        """Success updates window and keeps state closed."""
        ab = AdaptiveCircuitBreaker("test")
        ab.record_success()
        m = ab.metrics
        assert m.total_calls == 1
        assert m.success_rate == 1.0
        assert m.state == CircuitState.CLOSED

    def test_record_failure(self) -> None:
        """Failures update window and increase error count."""
        ab = AdaptiveCircuitBreaker("test", max_threshold=5)
        ab.record_failure(RuntimeError("fail"))
        m = ab.metrics
        assert m.total_calls == 1
        assert m.error_count == 1

    def test_threshold_lowers_on_high_error_rate(self) -> None:
        """Threshold decreases when error rate exceeds target."""
        ab = AdaptiveCircuitBreaker(
            "test",
            window_size=10,
            min_threshold=2,
            max_threshold=10,
            target_error_rate=0.1,
        )
        # Fill window with 80% failures
        for _ in range(8):
            ab.record_failure(RuntimeError("fail"))
        for _ in range(2):
            ab.record_success()

        assert ab.current_threshold < 10

    def test_threshold_stays_max_on_low_error_rate(self) -> None:
        """Threshold stays at max when error rate is below target."""
        ab = AdaptiveCircuitBreaker(
            "test",
            window_size=100,
            min_threshold=2,
            max_threshold=20,
            target_error_rate=0.1,
        )
        for _ in range(50):
            ab.record_success()

        assert ab.current_threshold == 20

    def test_trips_open_on_enough_failures(self) -> None:
        """Breaker opens after enough cumulative failures."""
        ab = AdaptiveCircuitBreaker(
            "test",
            min_threshold=2,
            max_threshold=3,
        )
        for _ in range(5):
            ab.record_failure(RuntimeError("fail"))

        assert ab.state == CircuitState.OPEN
        assert not ab.should_allow()

    def test_reset_clears_window(self) -> None:
        """Reset clears window and closes breaker."""
        ab = AdaptiveCircuitBreaker("test", max_threshold=3)
        for _ in range(5):
            ab.record_failure(RuntimeError("fail"))

        ab.reset()
        assert ab.state == CircuitState.CLOSED
        assert ab.metrics.total_calls == 0

    def test_metrics_snapshot(self) -> None:
        """Metrics returns correct snapshot."""
        ab = AdaptiveCircuitBreaker("test")
        ab.record_success()
        ab.record_success()
        ab.record_failure(RuntimeError("x"))

        m = ab.metrics
        assert isinstance(m, AdaptiveMetrics)
        assert m.total_calls == 3
        assert m.error_count == 1

    def test_on_threshold_change_callback(self) -> None:
        """Callback is invoked on threshold change."""
        changes: list[tuple[int, int]] = []

        ab = AdaptiveCircuitBreaker(
            "test",
            window_size=10,
            min_threshold=2,
            max_threshold=10,
            target_error_rate=0.1,
            on_threshold_change=lambda old, new: changes.append((old, new)),
        )
        # Cause high error rate to trigger threshold change
        for _ in range(9):
            ab.record_failure(RuntimeError("fail"))
        ab.record_success()

        assert len(changes) > 0

    def test_inner_breaker_access(self) -> None:
        """Can access the underlying CircuitBreaker."""
        ab = AdaptiveCircuitBreaker("test")
        assert ab.inner_breaker is not None
        assert ab.inner_breaker.name == "test"

    def test_empty_window_returns_max_threshold(self) -> None:
        """Empty window defaults to max threshold."""
        ab = AdaptiveCircuitBreaker(
            "test", min_threshold=2, max_threshold=15
        )
        assert ab.current_threshold == 15
