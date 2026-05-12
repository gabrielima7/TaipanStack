import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.circuit_breaker import CircuitBreakerError, circuit_breaker


class ChaosError(Exception):
    pass


@pytest.fixture
def chaos_breaker():
    @circuit_breaker(failure_threshold=3, timeout=0.1, failure_exceptions=(ChaosError,))
    def flaky_func(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(ChaosError("Simulated failure"))
        return Ok("Success")

    return flaky_func


def test_circuit_breaker_chaos_recovery(chaos_breaker):
    # Simulate 3 failures to open the circuit
    assert isinstance(chaos_breaker(True), Err)
    assert isinstance(chaos_breaker(True), Err)
    assert isinstance(chaos_breaker(True), Err)

    # Circuit should now be open, raising CircuitBreakerError
    with pytest.raises(CircuitBreakerError):
        chaos_breaker(False)
