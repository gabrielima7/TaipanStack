"""Tests for AdaptiveCircuitBreaker."""
from unittest.mock import patch

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.adaptive.adaptive_breaker import (
    AdaptiveCircuitBreaker,
    AdaptiveMetrics,
)
from taipanstack.resilience.circuit_breaker import CircuitState


class TestAdaptiveCircuitBreaker:
    """Tests for the adaptive circuit breaker."""

    def test_initial_state_closed_expected(self) -> None:
        """Starts in CLOSED state."""
        ab = AdaptiveCircuitBreaker("test")
        assert ab.state.value == CircuitState.CLOSED.value
        assert ab.should_allow()

    def test_adaptive_breaker_record_success_expected(self) -> None:
        """Success updates window and keeps state closed."""
        ab = AdaptiveCircuitBreaker("test")
        ab.record_success()
        m = ab.metrics
        assert m.total_calls == 1
        assert m.success_rate == 1.0
        assert m.state.value == CircuitState.CLOSED.value

    def test_record_failure_below_throughput_expected(self) -> None:
        """Failures update window, but don't trip if below min throughput."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=5, target_error_rate=0.1)
        for _ in range(4):
            ab.record_failure(RuntimeError("fail"))
        m = ab.metrics
        assert m.total_calls == 4
        assert m.error_count == 4
        assert m.state.value == CircuitState.CLOSED.value

    def test_trips_open_on_enough_failures_expected(self) -> None:
        """Breaker opens after enough cumulative failures (burst)."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=5, target_error_rate=0.5)
        for _ in range(6):
            ab.record_failure(RuntimeError("fail"))
        assert ab.state.value == CircuitState.OPEN.value
        assert not ab.should_allow()

    def test_stays_closed_if_under_target_rate_expected(self) -> None:
        """If error rate is below target, it stays closed even at high throughput."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=5, target_error_rate=0.5)
        for _ in range(6):
            ab.record_success()
        for _ in range(4):
            ab.record_failure(RuntimeError("fail"))
        assert ab.state.value == CircuitState.CLOSED.value
        assert ab.should_allow()

    def test_half_open_recovery_expected(self) -> None:
        """Breaker transitions to HALF_OPEN after timeout, then CLOSED on success."""
        with patch("taipanstack.resilience.adaptive.adaptive_breaker.time.monotonic") as mock_time:
            mock_time.return_value = 0.0
            ab = AdaptiveCircuitBreaker("test", min_throughput=2, target_error_rate=0.5, recovery_timeout=10.0)
            ab.record_failure(RuntimeError("fail"))
            ab.record_failure(RuntimeError("fail"))
            assert ab.state.value == CircuitState.OPEN.value
            mock_time.return_value = 11.0
            assert ab.state.value == CircuitState.HALF_OPEN.value
            assert ab.should_allow()
            ab.record_success()
            assert ab.state.value == CircuitState.CLOSED.value
            assert ab.metrics.total_calls == 1

    def test_half_open_failure_returns_to_open_expected(self) -> None:
        """Breaker transitions to HALF_OPEN after timeout, then back OPEN on failure."""
        with patch("taipanstack.resilience.adaptive.adaptive_breaker.time.monotonic") as mock_time:
            mock_time.return_value = 0.0
            ab = AdaptiveCircuitBreaker("test", min_throughput=2, target_error_rate=0.5, recovery_timeout=10.0)
            ab.record_failure(RuntimeError("fail"))
            ab.record_failure(RuntimeError("fail"))
            mock_time.return_value = 11.0
            assert ab.state.value == CircuitState.HALF_OPEN.value
            ab.record_failure(RuntimeError("fail"))
            assert ab.state.value == CircuitState.OPEN.value
            assert ab._last_opened_at == 11.0
            mock_time.return_value = 15.0
            assert ab.state.value == CircuitState.OPEN.value

    def test_reset_clears_window_expected(self) -> None:
        """Reset clears window and closes breaker."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=2, target_error_rate=0.1)
        ab.record_failure(RuntimeError("fail"))
        ab.record_failure(RuntimeError("fail"))
        assert ab.state.value == CircuitState.OPEN.value
        ab.reset()
        assert ab.state.value == CircuitState.CLOSED.value
        assert ab.metrics.total_calls == 0

    def test_adaptive_breaker_metrics_snapshot_expected(self) -> None:
        """Metrics returns correct snapshot."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=10, target_error_rate=0.9)
        ab.record_success()
        ab.record_success()
        ab.record_failure(RuntimeError("x"))
        m = ab.metrics
        assert isinstance(m, AdaptiveMetrics)
        assert m.total_calls == 3
        assert m.error_count == 1
        assert abs(m.error_rate - 1 / 3) < 1e-09
        assert abs(m.success_rate - 2 / 3) < 1e-09

    def test_evaluate_result_ok(self) -> None:
        """Evaluating an Ok result records success."""
        ab = AdaptiveCircuitBreaker("test")
        res = Ok(42)
        ret = ab.evaluate_result(res)
        assert ret is res
        assert ab.metrics.total_calls == 1
        assert ab.metrics.error_count == 0

    def test_evaluate_result_err_expected(self) -> None:
        """Evaluating an Err result records failure."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=2, target_error_rate=0.5)
        res = Err(ValueError("bad"))
        ret = ab.evaluate_result(res)
        assert ret is res
        assert ab.metrics.error_count == 1
        assert ab.metrics.total_calls == 1

    def test_adaptive_breaker_empty_metrics_expected(self) -> None:
        """Empty metrics return safe defaults."""
        ab = AdaptiveCircuitBreaker("test")
        m = ab.metrics
        assert m.total_calls == 0
        assert m.error_count == 0
        assert m.error_rate == 0.0
        assert m.success_rate == 1.0

    def test_adaptive_breaker_burst_scenario_expected(self) -> None:
        """Testing a burst scenario where error rates shift over a sliding window."""
        ab = AdaptiveCircuitBreaker("test", window_size=10, min_throughput=5, target_error_rate=0.5)
        for _ in range(10):
            ab.record_success()
        assert ab.state.value == CircuitState.CLOSED.value
        for _ in range(6):
            ab.record_failure(RuntimeError("burst"))
        assert ab.state.value == CircuitState.OPEN.value

def test_adaptive_breaker_err_branch_expected() -> None:
    from taipanstack.core.result import Err
    from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
    breaker = AdaptiveCircuitBreaker(name="test_err")
    breaker.evaluate_result(Err(ValueError("err")))
