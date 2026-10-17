
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.circuit_breaker import CircuitBreaker
from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_path_traversal,
    guard_ssrf,
)


def _risky_action_circuit_breaker(cb: CircuitBreaker, payload: str):
    if not cb.is_closed:
        return Err("Circuit Open")
    try:
        guard_command_injection([payload])
    except Exception as e:
        cb._record_failure(e)
        return Err(str(e))
    cb._record_success()
    return Ok(payload)


def test_integration_chaos():
    cb = CircuitBreaker(failure_threshold=2, timeout=0.1)

    # We shouldn't use retry on expected guard failures if we want circuit breaking,
    # but let's test just the circuit breaker

    res = _risky_action_circuit_breaker(cb, "echo hello")
    assert isinstance(res, Ok)

    # Trigger circuit breaker
    _risky_action_circuit_breaker(cb, "echo hello; rm -rf /")
    _risky_action_circuit_breaker(cb, "echo hello; rm -rf /")

    res = _risky_action_circuit_breaker(cb, "echo hello")
    assert isinstance(res, Err)
    assert res.err() == "Circuit Open"


@given(st.text(max_size=100))
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large])
def test_fuzz_guard_path_traversal(text):
    try:
        guard_path_traversal(text)
    except SecurityError:
        pass # Expected
    except Exception as e:
        pytest.fail(f"Unexpected exception type: {type(e)}")

@given(st.text(max_size=100))
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large])
def test_fuzz_guard_ssrf(text):
    try:
        guard_ssrf(text)
    except SecurityError:
        pass # Expected
    except Exception as e:
        pytest.fail(f"Unexpected exception type: {type(e)}")

def test_circuit_breaker_properties():
    cb = CircuitBreaker(failure_threshold=2)
    assert cb.is_closed is True
    assert cb.is_open is False
    assert cb.is_half_open is False
