import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
)


def test_circuit_breaker_lock_acquire_exception_decorator_sync():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            return None

    breaker._state.lock = BadLock()

    # Apply the logic the decorator applies
    @breaker
    def sync_func():
        return "success"

    assert sync_func() == "success"


@pytest.mark.asyncio
async def test_circuit_breaker_lock_acquire_exception_decorator_async():
    breaker = CircuitBreaker(failure_threshold=2)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            return None

    breaker._state.lock = BadLock()

    # Apply the logic the decorator applies
    @breaker
    async def async_func():
        return "success"

    assert (await async_func()) == "success"
