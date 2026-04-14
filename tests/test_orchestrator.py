"""Tests for the ResilienceOrchestrator."""

import asyncio

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.resilience.circuit_breaker import CircuitBreaker
from taipanstack.resilience.retry import RetryConfig

# --- helpers ----------------------------------------------------------------


async def _ok_fn() -> str:
    return "success"


async def _fail_fn() -> str:
    msg = "boom"
    raise RuntimeError(msg)


async def _slow_fn() -> str:
    await asyncio.sleep(5)
    return "slow"


# --- tests ------------------------------------------------------------------


class TestResilienceOrchestrator:
    """Tests for the orchestrator pipeline."""

    @pytest.mark.asyncio
    async def test_orchestrator_simple_execute_expected(self) -> None:
        """Executes a function without any patterns."""
        orch = ResilienceOrchestrator("test")
        result = await orch.execute(_ok_fn)
        assert isinstance(result, Ok)
        assert result.ok_value == "success"

    @pytest.mark.asyncio
    async def test_orchestrator_execute_failure_expected(self) -> None:
        """Returns Err on function failure."""
        orch = ResilienceOrchestrator("test")
        result = await orch.execute(_fail_fn)
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_orchestrator_with_timeout_expected(self) -> None:
        """Timeout triggers Err."""
        orch = ResilienceOrchestrator("test").with_timeout(0.05)
        result = await orch.execute(_slow_fn)
        assert isinstance(result, Err)
        assert "timed out" in str(result.err_value)

    @pytest.mark.asyncio
    async def test_orchestrator_with_fallback_expected(self) -> None:
        """Fallback replaces Err with Ok."""
        orch = ResilienceOrchestrator("test").with_fallback("cached")
        result = await orch.execute(_fail_fn)
        assert isinstance(result, Ok)
        assert result.ok_value == "cached"

    @pytest.mark.asyncio
    async def test_orchestrator_with_retry_expected(self) -> None:
        """Retries on failure then succeeds."""
        call_count = 0

        async def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                msg = "temp"
                raise RuntimeError(msg)
            return "ok"

        orch = ResilienceOrchestrator("test").with_retry(
            RetryConfig(max_attempts=3, initial_delay=0.01, jitter=False)
        )
        result = await orch.execute(flaky)
        assert isinstance(result, Ok)
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_orchestrator_with_circuit_breaker_expected(self) -> None:
        """Circuit breaker blocks calls when open."""
        breaker = CircuitBreaker(name="orch", failure_threshold=1)
        breaker._record_failure(Exception("trip"))

        orch = ResilienceOrchestrator("test").with_circuit_breaker(breaker)
        result = await orch.execute(_ok_fn)
        assert isinstance(result, Err)
        assert "open" in str(result.err_value).lower()

    @pytest.mark.asyncio
    async def test_orchestrator_with_adaptive_breaker_expected(self) -> None:
        """Adaptive breaker integrates with orchestrator."""
        ab = AdaptiveCircuitBreaker("orch", min_throughput=2, target_error_rate=0.5)
        for _ in range(5):
            ab.record_failure(RuntimeError("fail"))

        orch = ResilienceOrchestrator("test").with_circuit_breaker(ab)
        result = await orch.execute(_ok_fn)
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_orchestrator_adaptive_breaker_records_success_expected(self) -> None:
        """Successful execution records a success on the adaptive breaker."""
        ab = AdaptiveCircuitBreaker("orch", min_throughput=2, target_error_rate=0.5)
        orch = ResilienceOrchestrator("test").with_circuit_breaker(ab)

        result = await orch.execute(_ok_fn)

        assert isinstance(result, Ok)
        assert ab.metrics.total_calls == 1
        assert ab.metrics.error_count == 0

    @pytest.mark.asyncio
    async def test_orchestrator_adaptive_breaker_records_failure_expected(self) -> None:
        """Failing execution records a failure on the adaptive breaker."""
        ab = AdaptiveCircuitBreaker("orch", min_throughput=2, target_error_rate=0.5)
        orch = ResilienceOrchestrator("test").with_circuit_breaker(ab)

        result = await orch.execute(_fail_fn)

        assert isinstance(result, Err)
        assert ab.metrics.total_calls == 1
        assert ab.metrics.error_count == 1

    @pytest.mark.asyncio
    async def test_orchestrator_with_adaptive_retry_expected(self) -> None:
        """Adaptive retry integrates with orchestrator."""
        ar = AdaptiveRetry(min_delay=0.01, max_delay=0.1, max_attempts=3)
        ar.record_outcome(attempt=1, success=True, elapsed=0.01)

        call_count = 0

        async def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                msg = "fail"
                raise RuntimeError(msg)
            return "ok"

        orch = ResilienceOrchestrator("test").with_retry(ar)
        result = await orch.execute(flaky)
        assert isinstance(result, Ok)

    @pytest.mark.asyncio
    async def test_orchestrator_with_bulkhead_expected(self) -> None:
        """Bulkhead limits concurrency in pipeline."""
        orch = ResilienceOrchestrator("test").with_bulkhead(
            max_concurrent=2, max_queue=5
        )
        results = await asyncio.gather(*[orch.execute(_ok_fn) for _ in range(4)])
        assert all(isinstance(r, Ok) for r in results)

    @pytest.mark.asyncio
    async def test_bulkhead_queue_full_returns_err(self) -> None:
        """Queue saturation returns a bulkhead error before execution starts."""
        orch = ResilienceOrchestrator("test").with_bulkhead(
            max_concurrent=1, max_queue=0
        )

        result = await orch.execute(_ok_fn)

        assert isinstance(result, Err)
        assert "bulkhead" in str(result.err_value).lower()

    @pytest.mark.asyncio
    async def test_bulkhead_acquire_timeout_returns_err(self) -> None:
        """Semaphore acquisition timeout returns an error result."""
        orch = ResilienceOrchestrator("test").with_bulkhead(
            max_concurrent=1, max_queue=1, timeout=0.01
        )
        assert orch._bulkhead is not None
        await orch._bulkhead._semaphore.acquire()

        try:
            result = await orch.execute(_ok_fn)
        finally:
            orch._bulkhead._semaphore.release()

        assert isinstance(result, Err)
        assert "timed out" in str(result.err_value)

    @pytest.mark.asyncio
    async def test_orchestrator_full_pipeline_expected(self) -> None:
        """Full pipeline: bulkhead + breaker + retry + timeout + fallback."""
        call_count = 0

        async def sometimes_fails() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                msg = "first fail"
                raise RuntimeError(msg)
            return "recovered"

        orch = (
            ResilienceOrchestrator("full")
            .with_bulkhead(max_concurrent=5)
            .with_circuit_breaker(CircuitBreaker(name="full", failure_threshold=10))
            .with_retry(RetryConfig(max_attempts=3, initial_delay=0.01, jitter=False))
            .with_timeout(5.0)
            .with_fallback("fallback_value")
        )
        result = await orch.execute(sometimes_fails)
        assert isinstance(result, Ok)
        assert result.ok_value == "recovered"

    @pytest.mark.asyncio
    async def test_orchestrator_fallback_on_breaker_open_expected(self) -> None:
        """Fallback is applied when breaker is open."""
        breaker = CircuitBreaker(name="fb", failure_threshold=1)
        breaker._record_failure(Exception("trip"))

        orch = (
            ResilienceOrchestrator("test")
            .with_circuit_breaker(breaker)
            .with_fallback("safe")
        )
        result = await orch.execute(_ok_fn)
        assert isinstance(result, Ok)
        assert result.ok_value == "safe"

    @pytest.mark.asyncio
    async def test_orchestrator_retry_exhaustion_expected(self) -> None:
        """Returns Err when all retries fail."""
        orch = ResilienceOrchestrator("test").with_retry(
            RetryConfig(max_attempts=2, initial_delay=0.01, jitter=False)
        )
        result = await orch.execute(_fail_fn)
        assert isinstance(result, Err)

    @pytest.mark.asyncio
    async def test_zero_retry_attempts_returns_runtime_error(self) -> None:
        """A zero-attempt retry config returns the synthetic execution error."""
        orch = ResilienceOrchestrator("test").with_retry(
            RetryConfig(max_attempts=0, initial_delay=0.01, jitter=False)
        )

        result = await orch.execute(_ok_fn)

        assert isinstance(result, Err)
        assert isinstance(result.err_value, RuntimeError)
        assert str(result.err_value) == "Execution failed"

    @pytest.mark.asyncio
    async def test_orchestrator_chaining_returns_self_expected(self) -> None:
        """Builder methods return self for chaining."""
        orch = ResilienceOrchestrator("test")
        assert orch.with_bulkhead() is orch
        assert orch.with_timeout(1.0) is orch
        assert orch.with_fallback("x") is orch

    def test_orchestrator_apply_fallback_keeps_ok_result_expected(self) -> None:
        """Fallback logic leaves successful results untouched."""
        orch = ResilienceOrchestrator("test").with_fallback("cached")
        result = orch._apply_fallback(Ok("live"))

        assert isinstance(result, Ok)
        assert result.ok_value == "live"

    @pytest.mark.asyncio
    async def test_orchestrator_calculate_retry_delay_no_config_expected(self) -> None:
        orch = ResilienceOrchestrator("test")
        # Should return 0.0 when no retry config is set
        delay = orch._calculate_retry_delay(1)
        assert delay == 0.0


@pytest.mark.asyncio
async def test_orchestrator_fallback_err_branch_expected() -> None:
    from taipanstack.core.result import Ok
    from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator

    orchestrator = ResilienceOrchestrator("test_fallback").with_fallback(
        {"status": "failed"}
    )

    async def fail_func():
        raise ValueError("err")

    res = await orchestrator.execute(fail_func)
    assert res == Ok({"status": "failed"})


@pytest.mark.asyncio
async def test_orchestrator_execute_timeout_err_branch_expected() -> None:
    from taipanstack.core.result import Err
    from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
    from taipanstack.resilience.retry import RetryConfig

    # We want to test _execute_with_retry returning Err
    orchestrator = ResilienceOrchestrator("test_err").with_retry(
        RetryConfig(max_attempts=1)
    )

    async def fail_func():
        raise ValueError("err")

    res = await orchestrator.execute(fail_func)
    assert isinstance(res, Err)
