import pytest

from taipanstack.core.result import Err
from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_untracked_err_consistency_execution_success():
    breaker = CircuitBreaker(
        failure_threshold=1,
        success_threshold=2,
        timeout=0.01,
        failure_exceptions=(ValueError,),
    )

    @breaker
    def faulty_service_monad():
        return Err(KeyError("untracked failure"))

    @breaker
    def faulty_service_exc():
        raise KeyError("untracked failure")

    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = 0
    breaker._state.success_count = 0

    with pytest.raises(KeyError):
        faulty_service_exc()
    assert breaker._state.success_count == 0

    faulty_service_monad()
    assert breaker._state.success_count == 0


if __name__ == "__main__":
    test_chaos_circuit_breaker_untracked_err_consistency_execution_success()
