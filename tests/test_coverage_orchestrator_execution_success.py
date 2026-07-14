import asyncio

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.bulkhead import BulkheadFullError
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState
from taipanstack.resilience.retry import RetryConfig


@pytest.mark.asyncio
async def test_orchestrator_full_pipeline_success_execution_success():
    orch = (
        ResilienceOrchestrator()
        .with_bulkhead(max_concurrent=1)
        .with_circuit_breaker(AdaptiveCircuitBreaker())
        .with_retry(AdaptiveRetry(max_attempts=1))
        .with_timeout(1.0)
        .with_fallback("fallback")
    )

    async def success_fn():
        return "success"

    result = await orch.execute(success_fn)
    assert result == Ok("success")


@pytest.mark.asyncio
async def test_orchestrator_timeout_failure_execution_success():
    orch = ResilienceOrchestrator().with_timeout(0.01)

    async def slow_fn():
        await asyncio.sleep(0.1)
        return "slow"

    result = await orch.execute(slow_fn)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TimeoutError)


@pytest.mark.asyncio
async def test_orchestrator_circuit_breaker_open_execution_success():
    breaker = AdaptiveCircuitBreaker(min_throughput=1, target_error_rate=0.0)
    breaker.record_failure(ValueError("fail"))  # Open the breaker

    orch = ResilienceOrchestrator().with_circuit_breaker(breaker)

    async def fn():
        return "will not run"

    result = await orch.execute(fn)
    assert isinstance(result, Err)
    assert "is open" in str(result.err_value)


def test_orchestrator_invalid_timeout_execution_success():
    with pytest.raises(
        ValueError, match="timeout must be a finite non-negative number"
    ):
        ResilienceOrchestrator().with_timeout(-1.0)


@pytest.mark.asyncio
async def test_orchestrator_classic_circuit_breaker_execution_success():
    breaker = CircuitBreaker(failure_threshold=1)
    breaker._record_failure(ValueError("fail"))  # Open the breaker

    orch = ResilienceOrchestrator().with_circuit_breaker(breaker)

    async def fn():
        return "will not run"

    result = await orch.execute(fn)
    assert isinstance(result, Err)
    assert "is open" in str(result.err_value)


@pytest.mark.asyncio
async def test_orchestrator_classic_retry_config_execution_success():
    orch = ResilienceOrchestrator().with_retry(RetryConfig(max_attempts=3))

    attempts = 0

    async def failing_fn():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("fail")
        return "success"

    result = await orch.execute(failing_fn)
    assert result == Ok("success")
    assert attempts == 3


@pytest.mark.asyncio
async def test_orchestrator_fallback_on_error_execution_success():
    orch = ResilienceOrchestrator().with_fallback("default")

    async def failing_fn():
        raise ValueError("fail")

    result = await orch.execute(failing_fn)
    assert result == Ok("default")


@pytest.mark.asyncio
async def test_orchestrator_timeout_without_fallback_execution_success():
    orch = ResilienceOrchestrator().with_timeout(0.01)

    async def slow_fn():
        await asyncio.sleep(0.1)
        return "slow"

    result = await orch.execute(slow_fn)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TimeoutError)


@pytest.mark.asyncio
async def test_orchestrator_execute_returns_result_execution_success():
    orch = ResilienceOrchestrator()

    async def result_fn():
        return Ok("already ok")

    result = await orch.execute(result_fn)
    assert result == Ok("already ok")


@pytest.mark.asyncio
async def test_orchestrator_bulkhead_full_execution_success():
    orch = ResilienceOrchestrator().with_bulkhead(max_concurrent=1, max_queue=0)

    async def slow_fn():
        await asyncio.sleep(0.1)
        return "slow"

    # First call takes the permit
    task = asyncio.create_task(orch.execute(slow_fn))
    await asyncio.sleep(0.01)  # let the first task acquire the permit

    # Second call should immediately fail with BulkheadFullError
    result = await orch.execute(slow_fn)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, BulkheadFullError)

    await task  # wait for first task to complete


@pytest.mark.asyncio
async def test_orchestrator_bulkhead_timeout_execution_success():
    # Set a very low timeout for semaphore acquisition
    orch = ResilienceOrchestrator().with_bulkhead(
        max_concurrent=1, max_queue=5, timeout=0.01
    )

    async def slow_fn():
        await asyncio.sleep(0.1)
        return "slow"

    # First call takes the permit
    task = asyncio.create_task(orch.execute(slow_fn))
    await asyncio.sleep(0.01)  # let the first task acquire the permit

    # Second call gets queued, then times out waiting for the permit
    result = await orch.execute(slow_fn)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, TimeoutError)
    assert "timed out after" in str(result.err_value)

    await task  # wait for first task to complete


@pytest.mark.asyncio
async def test_orchestrator_circuit_breaker_exception_second_attempt_execution_success():
    breaker = AdaptiveCircuitBreaker(min_throughput=1, target_error_rate=0.0)
    # Open the breaker
    breaker.record_failure(ValueError("fail"))

    orch = (
        ResilienceOrchestrator()
        .with_retry(RetryConfig(max_attempts=2))
        .with_circuit_breaker(breaker)
    )

    async def fn():
        raise ValueError("first attempt fail")

    result = await orch.execute(fn)
    assert isinstance(result, Err)
    # the second attempt should trigger the breaker and handle it via cb_res Exception path
    # actually check_circuit_breaker_for_attempt only returns Exception if attempt > 1!


@pytest.mark.asyncio
async def test_orchestrator_circuit_breaker_exception_second_attempt_real_execution_success():
    breaker = AdaptiveCircuitBreaker(min_throughput=1, target_error_rate=0.0)

    orch = (
        ResilienceOrchestrator()
        .with_retry(RetryConfig(max_attempts=2))
        .with_circuit_breaker(breaker)
    )

    attempts = 0

    async def fn():
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            breaker.record_failure(
                ValueError("force open")
            )  # this will open the circuit during attempt 1
            raise ValueError("first attempt fail")
        return "success"

    result = await orch.execute(fn)
    assert isinstance(result, Err)
    assert "is open" in str(result.err_value)


@pytest.mark.asyncio
async def test_orchestrator_general_exceptions_execution_success():
    orch = ResilienceOrchestrator()

    async def failing_fn():
        raise RuntimeError("generic")

    result = await orch.execute(failing_fn)
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_orchestrator_general_exceptions_with_bulkhead_execution_success():
    orch = ResilienceOrchestrator().with_bulkhead(max_concurrent=1)

    async def failing_fn():
        raise RuntimeError("generic")

    result = await orch.execute(failing_fn)
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_orchestrator_max_attempts_zero_execution_success():
    # Covers the for-loop not executing
    orch = ResilienceOrchestrator().with_retry(RetryConfig(max_attempts=0))

    async def fn():
        return "test"

    result = await orch.execute(fn)
    assert isinstance(result, Err)
    assert "Execution failed" in str(result.err_value)


@pytest.mark.asyncio
async def test_orchestrator_bulkhead_invalid_timeout_execution_success():
    with pytest.raises(
        ValueError, match="timeout must be a finite non-negative number"
    ):
        ResilienceOrchestrator().with_bulkhead(timeout=-1.0)


@pytest.mark.asyncio
async def test_orchestrator_record_outcomes_with_adaptive_retry_execution_success():
    ar = AdaptiveRetry(max_attempts=3)
    orch = ResilienceOrchestrator().with_retry(ar)

    attempts = 0

    async def fn():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ValueError("fail first")
        return "success"

    await orch.execute(fn)
    # The adaptive retry should have received a failure and a success
    assert ar.metrics.total_outcomes == 2


@pytest.mark.asyncio
async def test_orchestrator_calculate_retry_delay_execution_success():
    # Covers _calculate_retry_delay when _retry_config is None
    orch = ResilienceOrchestrator()
    assert orch._calculate_retry_delay(1) == 0.0


@pytest.mark.asyncio
async def test_orchestrator_classic_circuit_breaker_record_success_execution_success():
    breaker = CircuitBreaker(failure_threshold=1)
    orch = ResilienceOrchestrator().with_circuit_breaker(breaker)

    async def fn():
        return "success"

    await orch.execute(fn)
    assert breaker.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_orchestrator_classic_circuit_breaker_record_failure_execution_success():
    breaker = CircuitBreaker(failure_threshold=1)
    orch = ResilienceOrchestrator().with_circuit_breaker(breaker)

    async def failing_fn():
        raise ValueError("fail")

    await orch.execute(failing_fn)
    assert breaker.state == CircuitState.OPEN


@pytest.mark.asyncio
async def test_orchestrator_execute_inner_exception_execution_success():
    # Make _execute_inner raise directly to hit line 230-231
    orch = ResilienceOrchestrator()

    import unittest.mock

    with unittest.mock.patch.object(
        orch, "_execute_inner", side_effect=Exception("inner fail")
    ):
        result = await orch.execute(lambda: "test")
        assert isinstance(result, Err)
        assert str(result.err_value) == "inner fail"


@pytest.mark.asyncio
async def test_orchestrator_execute_inner_exception_with_bulkhead_execution_success():
    # Make _execute_inner raise directly to hit line 222-223
    orch = ResilienceOrchestrator().with_bulkhead(max_concurrent=1)

    import unittest.mock

    with unittest.mock.patch.object(
        orch, "_execute_inner", side_effect=Exception("inner fail bh")
    ):
        result = await orch.execute(lambda: "test")
        assert isinstance(result, Err)
        assert str(result.err_value) == "inner fail bh"
