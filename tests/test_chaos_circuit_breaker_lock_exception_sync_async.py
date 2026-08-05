import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
)


def test_circuit_breaker_lock_acquire_exception_decorator_sync():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            pass

    breaker._state.lock = BadLock()

    # Apply the logic the decorator applies
    @breaker
    def sync_func():
        return "success"

    with pytest.raises(CircuitBreakerError, match="is open"):
        sync_func()


@pytest.mark.asyncio
async def test_circuit_breaker_lock_acquire_exception_decorator_async():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            pass

    breaker._state.lock = BadLock()

    # Apply the logic the decorator applies
    @breaker
    async def async_func():
        return "success"

    with pytest.raises(CircuitBreakerError, match="is open"):
        await async_func()
