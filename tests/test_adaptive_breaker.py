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

    def test_adaptive_breaker_initial_state_closed(self) -> None:
        """Starts in CLOSED state."""
        ab = AdaptiveCircuitBreaker("test")
        assert ab.state.value == CircuitState.CLOSED.value
        assert ab.should_allow()

    def test_adaptive_breaker_record_success(self) -> None:
        """Success updates window and keeps state closed."""
        ab = AdaptiveCircuitBreaker("test")
        ab.record_success()
        m = ab.metrics
        assert m.total_calls == 1
        assert m.success_rate == 1.0
        assert m.state.value == CircuitState.CLOSED.value

    def test_adaptive_breaker_record_failure_below_throughput(self) -> None:
        """Failures update window, but don't trip if below min throughput."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=5, target_error_rate=0.1)
        # 4 failures, 0 successes (100% error rate). Below 5 throughput.
        for _ in range(4):
            ab.record_failure(RuntimeError("fail"))

        m = ab.metrics
        assert m.total_calls == 4
        assert m.error_count == 4
        assert m.state.value == CircuitState.CLOSED.value

    def test_adaptive_breaker_trips_open_on_enough_failures(self) -> None:
        """Breaker opens after enough cumulative failures (burst)."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=5, target_error_rate=0.5)

        # We need more than 50% failures out of at least 5. Let's do 6 failures out of 6.
        for _ in range(6):
            ab.record_failure(RuntimeError("fail"))

        assert ab.state.value == CircuitState.OPEN.value
        assert not ab.should_allow()

    def test_adaptive_breaker_stays_closed_if_under_target_rate(self) -> None:
        """If error rate is below target, it stays closed even at high throughput."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=5, target_error_rate=0.5)

        # Do 10 requests: 6 successes, 4 failures (40% error rate).
        # We must do successes first so it doesn't trip on the 5th request (which would be 100% failure rate).
        for _ in range(6):
            ab.record_success()
        for _ in range(4):
            ab.record_failure(RuntimeError("fail"))

        assert ab.state.value == CircuitState.CLOSED.value
        assert ab.should_allow()

    def test_adaptive_breaker_half_open_recovery(self) -> None:
        """Breaker transitions to HALF_OPEN after timeout, then CLOSED on success."""
        with patch(
            "taipanstack.resilience.adaptive.adaptive_breaker.time.monotonic"
        ) as mock_time:
            # Time 0
            mock_time.return_value = 0.0
            ab = AdaptiveCircuitBreaker(
                "test", min_throughput=2, target_error_rate=0.5, recovery_timeout=10.0
            )

            # Trip it open
            ab.record_failure(RuntimeError("fail"))
            ab.record_failure(RuntimeError("fail"))
            assert ab.state.value == CircuitState.OPEN.value

            # Time 11: Past timeout, should go to half-open
            mock_time.return_value = 11.0
            assert ab.state.value == CircuitState.HALF_OPEN.value
            assert ab.should_allow()

            # Successful call should close it
            ab.record_success()
            assert ab.state.value == CircuitState.CLOSED.value
            assert ab.metrics.total_calls == 1  # Just the success

    def test_adaptive_breaker_half_open_failure_returns_to_open(self) -> None:
        """Breaker transitions to HALF_OPEN after timeout, then back OPEN on failure."""
        with patch(
            "taipanstack.resilience.adaptive.adaptive_breaker.time.monotonic"
        ) as mock_time:
            # Time 0
            mock_time.return_value = 0.0
            ab = AdaptiveCircuitBreaker(
                "test", min_throughput=2, target_error_rate=0.5, recovery_timeout=10.0
            )

            ab.record_failure(RuntimeError("fail"))
            ab.record_failure(RuntimeError("fail"))

            # Time 11: Past timeout, should go to half-open
            mock_time.return_value = 11.0
            assert ab.state.value == CircuitState.HALF_OPEN.value

            # Failure puts it back to open
            ab.record_failure(RuntimeError("fail"))
            assert ab.state.value == CircuitState.OPEN.value
            assert ab._last_opened_at == 11.0  # Last opened updated

            # At time 15 it's still open
            mock_time.return_value = 15.0
            assert ab.state.value == CircuitState.OPEN.value

    def test_adaptive_breaker_reset_clears_window(self) -> None:
        """Reset clears window and closes breaker."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=2, target_error_rate=0.1)
        ab.record_failure(RuntimeError("fail"))
        ab.record_failure(RuntimeError("fail"))

        assert ab.state.value == CircuitState.OPEN.value
        ab.reset()
        assert ab.state.value == CircuitState.CLOSED.value
        assert ab.metrics.total_calls == 0

    def test_adaptive_breaker_metrics_snapshot(self) -> None:
        """Metrics returns correct snapshot."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=10, target_error_rate=0.9)
        ab.record_success()
        ab.record_success()
        ab.record_failure(RuntimeError("x"))

        m = ab.metrics
        assert isinstance(m, AdaptiveMetrics)
        assert m.total_calls == 3
        assert m.error_count == 1
        assert abs(m.error_rate - 1 / 3) < 1e-9
        assert abs(m.success_rate - 2 / 3) < 1e-9

    def test_adaptive_breaker_evaluate_result_ok(self) -> None:
        """Evaluating an Ok result records success."""
        ab = AdaptiveCircuitBreaker("test")
        res = Ok(42)
        ret = ab.evaluate_result(res)
        assert ret is res
        assert ab.metrics.total_calls == 1
        assert ab.metrics.error_count == 0

    def test_adaptive_breaker_evaluate_result_err(self) -> None:
        """Evaluating an Err result records failure."""
        ab = AdaptiveCircuitBreaker("test", min_throughput=2, target_error_rate=0.5)
        res = Err(ValueError("bad"))
        ret = ab.evaluate_result(res)
        assert ret is res
        assert ab.metrics.error_count == 1
        assert ab.metrics.total_calls == 1

    def test_adaptive_breaker_empty_metrics(self) -> None:
        """Empty metrics return safe defaults."""
        ab = AdaptiveCircuitBreaker("test")
        m = ab.metrics
        assert m.total_calls == 0
        assert m.error_count == 0
        assert m.error_rate == 0.0
        assert m.success_rate == 1.0

    def test_adaptive_breaker_burst_scenario(self) -> None:
        """Testing a burst scenario where error rates shift over a sliding window."""
        # Window size 10, min throughput 5, trip at 50% failures
        ab = AdaptiveCircuitBreaker(
            "test", window_size=10, min_throughput=5, target_error_rate=0.5
        )

        # 10 successes
        for _ in range(10):
            ab.record_success()

        assert ab.state.value == CircuitState.CLOSED.value

        # 6 failures push the oldest 6 successes out
        for _ in range(6):
            ab.record_failure(RuntimeError("burst"))

        # The window is now: [True, True, True, True, False, False, False, False, False, False]
        # Total: 10, Errors: 6 -> Error rate 60% -> Tripped!
        assert ab.state.value == CircuitState.OPEN.value


def test_adaptive_breaker_err_branch() -> None:
    from taipanstack.core.result import Err
    from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker

    breaker = AdaptiveCircuitBreaker(name="test_err")
    breaker.evaluate_result(Err(ValueError("err")))


# Migrated from tests/test_chaos_circuit_breaker_nan_operations.py
import pytest

from taipanstack.resilience.adaptive.bulkhead import Bulkhead
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_nan_failure_threshold():
    """Chaos test: Inject NaN for failure_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(failure_threshold=float("nan"))


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_nan_success_threshold():
    """Chaos test: Inject NaN for success_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(success_threshold=float("nan"))


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_inf_failure_threshold():
    """Chaos test: Inject Inf for failure_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(failure_threshold=float("inf"))


def test_chaos_circuit_breaker_nan_circuit_breaker_rejects_inf_success_threshold():
    """Chaos test: Inject Inf for success_threshold."""
    with pytest.raises(ValueError, match="must be a finite"):
        CircuitBreaker(success_threshold=float("inf"))


def test_chaos_circuit_breaker_nan_adaptive_breaker_rejects_nan_recovery_timeout():
    """Chaos test: Inject NaN for recovery timeout."""
    with pytest.raises(ValueError, match="must be a finite"):
        AdaptiveCircuitBreaker(recovery_timeout=float("nan"))


def test_chaos_circuit_breaker_nan_bulkhead_rejects_nan_timeout():
    """Chaos test: Inject NaN for timeout."""
    with pytest.raises(ValueError, match="must be a finite"):
        Bulkhead("default", timeout=float("nan"))


def test_chaos_circuit_breaker_nan_orchestrator_rejects_nan_timeout():
    """Chaos test: Inject NaN for orchestrator timeout."""
    with pytest.raises(ValueError, match="must be a finite"):
        ResilienceOrchestrator().with_timeout(float("nan"))


def test_chaos_circuit_breaker_nan_orchestrator_with_bulkhead_rejects_nan_timeout():
    """Chaos test: Inject NaN for orchestrator bulkhead timeout."""
    with pytest.raises(ValueError, match="finite non-negative number"):
        ResilienceOrchestrator().with_bulkhead(timeout=float("nan"))
