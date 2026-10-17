import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


class ExceptionLock:
    def acquire(self, timeout: float = -1) -> bool:
        raise MemoryError("Out of memory!")

    def release(self) -> None:
        raise MemoryError("Out of memory!")

def test_chaos_circuit_breaker_lock_exception_sync():
    breaker = CircuitBreaker(failure_threshold=1)
    breaker._state.lock = ExceptionLock()

    @breaker
    def ok_func_sync():
        return True

    with pytest.raises(CircuitBreakerError) as exc_info:
        ok_func_sync()

    assert exc_info.value.state == CircuitState.CLOSED

class BaseExceptionLock:
    def acquire(self, timeout: float = -1) -> bool:
        raise BaseException("System level error")

    def release(self) -> None:
        raise BaseException("System level error")

def test_chaos_circuit_breaker_lock_base_exception_sync():
    breaker = CircuitBreaker(failure_threshold=1)
    breaker._state.lock = BaseExceptionLock()

    @breaker
    def ok_func_sync():
        return True

    # Now that we catch BaseException and return False,
    # the wrapper will raise CircuitBreakerError!
    with pytest.raises(CircuitBreakerError):
        ok_func_sync()

def test_chaos_circuit_breaker_lock_base_exception_release():
    class BadReleaseLock:
        def acquire(self, timeout: float = -1) -> bool:
            return True

        def release(self) -> None:
            raise BaseException("Crash on release")

    breaker = CircuitBreaker(failure_threshold=1)
    breaker._state.lock = BadReleaseLock()

    @breaker
    def ok_func_sync():
        return True

    # The release error is caught and ignored in _safe_release,
    # so the function call should just succeed.
    assert ok_func_sync() is True

def test_chaos_circuit_breaker_lock_critical_exceptions():
    class CriticalExceptionLock:
        def acquire(self, timeout: float = -1) -> bool:
            raise KeyboardInterrupt("Interrupt")

        def release(self) -> None:
            raise SystemExit("Exit")

    breaker = CircuitBreaker(failure_threshold=1)
    breaker._state.lock = CriticalExceptionLock()

    @breaker
    def ok_func_sync():
        return True

    with pytest.raises(KeyboardInterrupt):
        ok_func_sync()

    # test release directly
    breaker._state.lock = CriticalExceptionLock()
    with pytest.raises(SystemExit):
        breaker._safe_release()

