import pytest

from taipanstack.core.result import Err
from taipanstack.resilience.circuit_breaker import CircuitBreaker


def test_chaos_circuit_breaker_exceptions_mutation_chaos_circuit_breaker_type_mutation_failure_exceptions():
    cb = CircuitBreaker()
    object.__setattr__(cb.config, "failure_exceptions", "corrupted")
    # Should not crash with TypeError
    res = cb._process_result(Err(ValueError("test")))
    assert isinstance(res, Err)


def test_chaos_circuit_breaker_exceptions_mutation_chaos_circuit_breaker_type_mutation_excluded_exceptions():
    cb = CircuitBreaker()
    object.__setattr__(cb.config, "excluded_exceptions", "corrupted")
    # Should not crash with TypeError
    cb._record_failure(ValueError("test"))


def test_chaos_circuit_breaker_exceptions_mutation_chaos_circuit_breaker_type_mutation_failure_exceptions_sync_raise():
    cb = CircuitBreaker()
    object.__setattr__(cb.config, "failure_exceptions", "corrupted")

    @cb
    def failing_func():
        raise ValueError("test")

    with pytest.raises(ValueError):
        failing_func()


@pytest.mark.asyncio
async def test_chaos_circuit_breaker_type_mutation_failure_exceptions_async_raise():
    cb = CircuitBreaker()
    object.__setattr__(cb.config, "failure_exceptions", "corrupted")

    @cb
    async def failing_func():
        raise ValueError("test")

    with pytest.raises(ValueError):
        await failing_func()


def test_chaos_circuit_breaker_exceptions_mutation_chaos_circuit_breaker_type_mutation_failure_exceptions_sync_raise_not_failure():
    cb = CircuitBreaker(failure_exceptions=(TypeError,))

    @cb
    def failing_func():
        raise ValueError("test")

    with pytest.raises(ValueError):
        failing_func()


@pytest.mark.asyncio
async def test_chaos_circuit_breaker_type_mutation_failure_exceptions_async_raise_not_failure():
    cb = CircuitBreaker(failure_exceptions=(TypeError,))

    @cb
    async def failing_func():
        raise ValueError("test")

    with pytest.raises(ValueError):
        await failing_func()
