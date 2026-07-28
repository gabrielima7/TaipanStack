import pytest
import threading

from taipanstack.core.result import Ok
from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    circuit_breaker,
)

def test_chaos_circuit_breaker_lock_exhaustion_chaos_circuit_breaker_lock_acquire_exception_sync():
    breaker = CircuitBreaker(failure_threshold=2)

    class BrokenLock:
        def acquire(self, timeout=-1):
            return False

        def release(self):
            pass

    breaker._state.lock = BrokenLock()
    assert breaker._should_attempt() is False
    breaker._record_success()
    breaker._record_failure(ValueError("test error"))
    breaker.reset()
    breaker._decrement_half_open(True)

    # Coverage for the Exception fallback path in acquire:
    class ExceptionalLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Out of memory")
        def release(self): pass

    breaker._state.lock = ExceptionalLock()
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

    breaker = None
    if hasattr(my_func, "__closure__") and my_func.__closure__:
        for cell in my_func.__closure__:
            if isinstance(cell.cell_contents, CircuitBreaker):
                breaker = cell.cell_contents
                break

    assert breaker is not None

    class BrokenLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Out of memory")
        def release(self): pass

    breaker._state.lock = BrokenLock()
    with pytest.raises(CircuitBreakerError, match="is open"):
        await my_func()


def test_chaos_circuit_breaker_lock_exhaustion_chaos_circuit_breaker_decorator_lock_acquire_exception_sync():
    @circuit_breaker(failure_threshold=2)
    def my_func():
        return Ok("success")

    breaker = None
    if hasattr(my_func, "__closure__") and my_func.__closure__:
        for cell in my_func.__closure__:
            if isinstance(cell.cell_contents, CircuitBreaker):
                breaker = cell.cell_contents
                break

    assert breaker is not None

    class BrokenLock:
        def acquire(self, timeout=-1):
            raise MemoryError("Out of memory")
        def release(self): pass

    breaker._state.lock = BrokenLock()
    with pytest.raises(CircuitBreakerError, match="is open"):
        my_func()
