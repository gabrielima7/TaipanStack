import contextlib

import pytest

from taipanstack.core.result import Result
from taipanstack.resilience.circuit_breaker import CircuitState, circuit_breaker
from taipanstack.resilience.retry import RetryError, retry


class ChaosError(Exception):
    def __str__(self):
        raise RuntimeError("Chaos stringification error")

def test_retry_chaos_exception_str_crash():
    @retry(max_attempts=2, on=(ChaosError,))
    def flaky_function() -> Result[int, Exception]:
        raise ChaosError("evil")

    try:
        flaky_function()
        pytest.fail("Retry should raise the exception after max attempts if reraise is True")
    except RuntimeError as e:
        if str(e) == "Chaos stringification error":
            pytest.fail("Retry crashed due to str(exc) in logging")
        else:
            raise
    except RetryError:
        pass # Expected
    except ChaosError:
        pass # Expected


def test_circuit_breaker_chaos_exception_str_crash():
    def corrupt_callback(old: CircuitState, new: CircuitState):
        raise ChaosError("evil")

    @circuit_breaker(failure_threshold=1, on_state_change=corrupt_callback)
    def failing_function():
        raise RuntimeError("trigger circuit breaker")

    try:
        failing_function()
    except Exception as e:
        if isinstance(e, RuntimeError) and str(e) == "Chaos stringification error":
            pytest.fail("Circuit breaker crashed due to str(exc) in callback failure logging")


def test_retry_chaos_exception_str_unprintable():
    @retry(max_attempts=2, on=(ChaosError,))
    def flaky_function() -> Result[int, Exception]:
        class UnprintableError(ChaosError):
            def __repr__(self):
                raise RuntimeError("Chaos repr error")
        raise UnprintableError("evil")

    with contextlib.suppress(RetryError):
        flaky_function()

def test_circuit_breaker_chaos_exception_str_unprintable():
    class UnprintableError(ChaosError):
        def __repr__(self):
            raise RuntimeError("Chaos repr error")

    def corrupt_callback(old: CircuitState, new: CircuitState):
        raise UnprintableError("evil")

    @circuit_breaker(failure_threshold=1, on_state_change=corrupt_callback)
    def failing_function():
        raise RuntimeError("trigger circuit breaker")

    with contextlib.suppress(Exception):
        failing_function()
