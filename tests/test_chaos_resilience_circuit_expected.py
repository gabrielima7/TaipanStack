import sys
import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)


def test_chaos_resilience_circuit_circuit_breaker_on_state_change_chaos_expected():
    """Simulate a chaos scenario where the user-provided callback fails.

    If a user provides an `on_state_change` callback that raises an unhandled
    exception during a critical state transition (e.g., OPEN to HALF_OPEN or
    HALF_OPEN to CLOSED), the circuit breaker should catch it, log it, and
    safely complete its state transition without bubbling the error up to the
    caller or corrupting its internal state.
    """

    def faulty_callback(old: CircuitState, new: CircuitState) -> None:
        # Simulate a rare memory limit or unexpected attribute error
        raise ValueError("Simulated adversarial failure in callback")

    # Configure a breaker that fails quickly
    breaker = CircuitBreaker(
        failure_threshold=1,
        success_threshold=1,
        timeout=0.01,
        on_state_change=faulty_callback,
    )

    @breaker
    def failing_service():
        raise RuntimeError("Service failure")

    @breaker
    def successful_service():
        return "success"

    # Trip the circuit (CLOSED -> OPEN). The faulty callback will trigger.
    # If the system isn't hardened, this will raise ValueError instead of returning normally,
    # OR it will corrupt the state.
    with pytest.raises(RuntimeError, match="Service failure"):
        failing_service()

    # Verify state transitioned successfully despite the callback exception
    assert breaker.state == CircuitState.OPEN

    # Wait for timeout to expire so we can transition to HALF_OPEN
    time.sleep(0.05)

    # Make a successful call. This will trigger a transition from OPEN -> HALF_OPEN
    # and then, because success_threshold=1, from HALF_OPEN -> CLOSED.
    # The callback will be fired twice and raise ValueError twice!
    # If unhandled, it will bubble up and crash the caller instead of returning "success".
    result = successful_service()

    assert result == "success"
    assert breaker.state == CircuitState.CLOSED


def test_chaos_resilience_circuit_circuit_breaker_on_state_change_chaos_without_structlog_expected(
    monkeypatch,
):
    """Test the failure branch when structlog is missing."""

    # We patch the module-level variable by grabbing the actual module
    # since it shares a name with the function.

    monkeypatch.setattr(
        sys.modules["taipanstack.resilience.circuit_breaker"], "_HAS_STRUCTLOG", False
    )

    def faulty_callback(old: CircuitState, new: CircuitState) -> None:
        raise ValueError("Simulated failure without structlog")

    breaker = CircuitBreaker(
        failure_threshold=1,
        success_threshold=1,
        timeout=0.01,
        on_state_change=faulty_callback,
    )

    @breaker
    def failing_service():
        raise RuntimeError("Service failure")

    with pytest.raises(RuntimeError, match="Service failure"):
        failing_service()

    assert breaker.state == CircuitState.OPEN


def test_chaos_resilience_circuit_circuit_breaker_chaos_config_mutations_expected():
    """Test chaos: Invalid configuration values cause fast failure.

    If instantiated with NaN timeout, negative timeout, or 0 thresholds,
    the CircuitBreaker should refuse to initialize instead of failing
    silently or getting stuck in an undefined state.
    """

    with pytest.raises(
        ValueError, match="timeout must be a finite non-negative number"
    ):
        CircuitBreaker(timeout=float("nan"))

    with pytest.raises(
        ValueError, match="timeout must be a finite non-negative number"
    ):
        CircuitBreaker(timeout=-1.0)

    with pytest.raises(
        ValueError, match="failure_threshold must be a finite number >= 1"
    ):
        CircuitBreaker(failure_threshold=0)

    with pytest.raises(
        ValueError, match="success_threshold must be a finite number >= 1"
    ):
        CircuitBreaker(success_threshold=0)


def test_chaos_resilience_circuit_structlog_warning_without_callback_expected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """State transition logs through structlog when no callback is set."""
    import importlib

    cb_mod = importlib.import_module("taipanstack.resilience.circuit_breaker")
    from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

    class LoggerStub:
        def __init__(self) -> None:
            self.calls = 0

        def warning(self, *args: object, **kwargs: object) -> None:
            self.calls += 1

    logger = LoggerStub()
    monkeypatch.setattr(cb_mod, "_HAS_STRUCTLOG", True)
    monkeypatch.setattr(cb_mod, "_structlog_logger", logger)

    cb = CircuitBreaker(failure_threshold=1, timeout=0.1)
    cb._notify_state_change(CircuitState.CLOSED, CircuitState.OPEN)
    assert logger.calls == 1


def test_chaos_resilience_circuit_structlog_fallback_noop_when_unavailable_expected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No structlog call occurs when fallback logger is unavailable."""
    import importlib

    cb_mod = importlib.import_module("taipanstack.resilience.circuit_breaker")
    from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

    monkeypatch.setattr(cb_mod, "_HAS_STRUCTLOG", False)
    monkeypatch.setattr(cb_mod, "_structlog_logger", None)

    cb = CircuitBreaker(failure_threshold=1, timeout=0.1)
    cb._notify_state_change(CircuitState.CLOSED, CircuitState.OPEN)
