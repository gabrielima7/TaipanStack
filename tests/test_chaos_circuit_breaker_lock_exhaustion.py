import pytest

from taipanstack.core.result import Ok
from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    circuit_breaker,
)


def test_chaos_circuit_breaker_lock_exhaustion_chaos_circuit_breaker_lock_acquire_exception_sync_expected():
    breaker = CircuitBreaker(failure_threshold=2)

    class BrokenLock:
        def __enter__(self):
            raise MemoryError("Out of memory")

        def __exit__(self, _exc_type, _exc_val, _exc_tb):
            return False

    breaker._state.lock = BrokenLock()
    assert breaker._should_attempt() is False
    breaker._record_success()
    breaker._record_failure(ValueError("test error"))
    breaker.reset()
    breaker._decrement_half_open(True)


@pytest.mark.asyncio
async def test_chaos_circuit_breaker_lock_exhaustion_chaos_circuit_breaker_decorator_lock_acquire_exception_async():
    @circuit_breaker(failure_threshold=2)
    async def my_func():
        return Ok("success")

    breaker_instance = my_func.__closure__[1].cell_contents

    class BrokenLock:
        def __enter__(self):
            raise MemoryError("Out of memory")

        def __exit__(self, _exc_type, _exc_val, _exc_tb):
            return False

    breaker_instance._state.lock = BrokenLock()
    with pytest.raises(CircuitBreakerError, match="is open"):
        await my_func()


def test_chaos_circuit_breaker_lock_exhaustion_chaos_circuit_breaker_decorator_lock_acquire_exception_sync_expected():
    @circuit_breaker(failure_threshold=2)
    def my_func():
        return Ok("success")

    breaker_instance = my_func.__closure__[1].cell_contents

    class BrokenLock:
        def __enter__(self):
            raise MemoryError("Out of memory")

        def __exit__(self, _exc_type, _exc_val, _exc_tb):
            return False

    breaker_instance._state.lock = BrokenLock()
    with pytest.raises(CircuitBreakerError, match="is open"):
        my_func()
