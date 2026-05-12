import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_circuit_breaker_type_corruption():
    breaker = CircuitBreaker(failure_threshold=3, timeout=0.1)

    # Intentionally corrupt the state's internal counters to simulate severe memory/type mutation
    breaker._state.failure_count = "corrupted_string"  # type: ignore

    # When we try to record a failure, it should safely handle the TypeError
    try:
        breaker._record_failure(Exception("test"))
    except TypeError:
        pytest.fail(
            "CircuitBreaker crashed on corrupted state instead of safe degradation"
        )

    # The _update_failure_metrics degraded safely, let's see if circuit is open
    assert breaker.state.value == "open", "Circuit should fail-open on type corruption"
