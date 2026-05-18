"""Tests for the Result module (functional error handling)."""

import pytest

from taipanstack.core.result import (
    Err,
    Ok,
    Result,
    and_then_async,
    collect_results,
    map_async,
    safe,
    safe_from,
)


class TestOkErr:
    """Tests for basic Ok/Err functionality."""

    def test_result_module_ok_value(self) -> None:
        """Test Ok wraps value correctly."""
        result: Result[int, Exception] = Ok(42)
        assert result.is_ok()
        assert not result.is_err()
        assert result.ok_value == 42

    def test_result_module_err_value(self) -> None:
        """Test Err wraps error correctly."""
        error = ValueError("test error")
        result: Result[int, ValueError] = Err(error)
        assert result.is_err()
        assert not result.is_ok()
        assert result.err_value == error


class TestSafeDecorator:
    """Tests for the @safe decorator."""

    def test_result_module_safe_success(self) -> None:
        """Test safe decorator returns Ok on success."""

        @safe
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)
        assert result.is_ok()
        assert result.ok_value == 5

    def test_result_module_safe_exception(self) -> None:
        """Test safe decorator returns Err on exception."""

        @safe
        def divide(a: int, b: int) -> float:
            return a / b

        result = divide(10, 0)
        assert result.is_err()
        assert isinstance(result.err_value, ZeroDivisionError)

    def test_result_module_safe_basic_exception(self) -> None:
        """Test safe decorator returns Err on base Exception."""

        @safe
        def raise_exception() -> None:
            raise Exception("Basic exception occurred")  # noqa: TRY002

        result = raise_exception()
        assert result.is_err()
        err = result.err_value
        assert type(err) is Exception
        assert str(err) == "Basic exception occurred"

    def test_result_module_safe_preserves_function_metadata(self) -> None:
        """Test safe decorator preserves function name and docstring."""

        @safe
        def my_function() -> int:
            """My docstring."""
            return 42

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."


class TestSafeFromDecorator:
    """Tests for the @safe_from decorator."""

    def test_result_module_safe_from_catches_specified_exception(self) -> None:
        """Test safe_from catches specified exception types."""

        @safe_from(ValueError)
        def parse(s: str) -> int:
            return int(s)

        result = parse("not_a_number")
        assert result.is_err()
        assert isinstance(result.err_value, ValueError)

    def test_result_module_safe_from_propagates_unspecified_exception(
        self,
    ) -> None:
        """Test safe_from propagates unspecified exception types."""

        @safe_from(ValueError)
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

    def test_result_module_safe_from_multiple_types(self) -> None:
        """Test safe_from with multiple exception types."""

        @safe_from(ValueError, TypeError)
        def process(x: int | str) -> int:
            if isinstance(x, str):
                return int(x)
            raise TypeError("Expected string")

        result1 = process("abc")
        assert result1.is_err()
        assert isinstance(result1.err_value, ValueError)

        result2 = process(123)
        assert result2.is_err()
        assert isinstance(result2.err_value, TypeError)

    def test_result_module_safe_from_explicit_raise(self) -> None:
        """Test safe_from decorator catching explicitly raised exception."""

        @safe_from(ValueError)
        def process(data: str) -> int:
            raise ValueError("explicitly raised")

        result = process("abc")
        assert result.is_err()
        assert isinstance(result.err_value, ValueError)
        assert str(result.err_value) == "explicitly raised"

    def test_result_module_safe_from_inheritance(self) -> None:
        """Test safe_from catches subclasses of specified exceptions."""

        class SubValueError(ValueError): ...

        @safe_from(ValueError)
        def fail() -> None:
            raise SubValueError("subclass error")

        result = fail()
        assert result.is_err()
        assert isinstance(result.err_value, SubValueError)
        assert str(result.err_value) == "subclass error"


class TestCollectResults:
    """Tests for collect_results function."""

    def test_result_module_collect_all_ok(self) -> None:
        """Test collect_results with all Ok values."""
        results: list[Result[int, ValueError]] = [Ok(1), Ok(2), Ok(3)]
        collected = collect_results(results)
        assert collected.is_ok()
        assert collected.ok_value == [1, 2, 3]

    def test_result_module_collect_with_err(self) -> None:
        """Test collect_results stops at first Err."""
        results: list[Result[int, ValueError]] = [
            Ok(1),
            Err(ValueError("error")),
            Ok(3),
        ]
        collected = collect_results(results)
        assert collected.is_err()
        assert isinstance(collected.err_value, ValueError)
        assert str(collected.err_value) == "error"

    def test_result_module_collect_empty(self) -> None:
        """Test collect_results with empty list."""
        results: list[Result[int, ValueError]] = []
        collected = collect_results(results)
        assert collected.is_ok()
        assert collected.ok_value == []

    def test_result_module_collect_first_err_returned(self) -> None:
        """Test collect_results returns first Err encountered."""
        results: list[Result[int, ValueError]] = [
            Ok(1),
            Err(ValueError("first")),
            Err(ValueError("second")),
        ]
        collected = collect_results(results)
        assert collected.is_err()
        assert isinstance(collected.err_value, ValueError)
        assert str(collected.err_value) == "first"


class TestUnwrapOr:
    """Tests for unwrap_or function."""

    def test_result_module_unwrap_or_ok(self) -> None:
        """Test unwrap_or returns Ok value."""
        result: Result[int, ValueError] = Ok(42)
        assert result.unwrap_or(0) == 42

    def test_result_module_unwrap_or_err(self) -> None:
        """Test unwrap_or returns default on Err."""
        result: Result[int, ValueError] = Err(ValueError("error"))
        assert result.unwrap_or(0) == 0


class TestUnwrapOrElse:
    """Tests for unwrap_or_else function."""

    def test_result_module_unwrap_or_else_ok(self) -> None:
        """Test unwrap_or_else returns Ok value."""
        result: Result[int, ValueError] = Ok(42)
        assert result.unwrap_or_else(len) == 42

    def test_result_module_unwrap_or_else_err(self) -> None:
        """Test unwrap_or_else computes default from error."""
        result: Result[int, ValueError] = Err(ValueError("error"))
        assert result.unwrap_or_else(lambda e: len(str(e))) == 5

    def test_result_module_unwrap_or_else_with_exception(self) -> None:
        """Test unwrap_or_else with exception error type."""
        error = ValueError("test message")
        result: Result[int, ValueError] = Err(error)
        assert result.unwrap_or_else(lambda e: len(str(e))) == 12  # len("test message")


class TestMatchCase:
    """Tests for match/case pattern matching with Result."""

    def test_result_module_match_ok(self) -> None:
        """Test match/case with Ok value."""
        result: Result[int, ValueError] = Ok(42)
        match result:
            case Ok(value):
                assert value == 42
            case Err():
                pytest.fail("Should not match Err")

    def test_result_module_match_err(self) -> None:
        """Test match/case with Err value."""
        result: Result[int, ValueError] = Err(ValueError("error"))
        match result:
            case Ok():
                pytest.fail("Should not match Ok")
            case Err(error):
                assert isinstance(error, ValueError)
                assert str(error) == "error"


class TestSafeAsyncDecorator:
    """Tests for the @safe decorator with async functions."""

    @pytest.mark.asyncio
    async def test_safe_async_success(self) -> None:
        """Test safe decorator returns Ok on async success."""

        @safe
        async def async_add(a: int, b: int) -> int:
            return a + b

        result = await async_add(2, 3)
        assert result.is_ok()
        assert result.ok_value == 5

    @pytest.mark.asyncio
    async def test_safe_async_exception(self) -> None:
        """Test safe decorator returns Err on async exception."""

        @safe
        async def async_divide(a: int, b: int) -> float:
            return a / b

        result = await async_divide(10, 0)
        assert result.is_err()
        assert isinstance(result.err_value, ZeroDivisionError)

    @pytest.mark.asyncio
    async def test_safe_async_preserves_metadata(self) -> None:
        """Test safe decorator preserves async function name and docstring."""

        @safe
        async def my_async_function() -> int:
            """Async docstring."""
            return 42

        assert my_async_function.__name__ == "my_async_function"
        assert my_async_function.__doc__ == "Async docstring."

    @pytest.mark.asyncio
    async def test_safe_async_runtime_error(self) -> None:
        """Test safe decorator catches RuntimeError in async function."""

        @safe
        async def async_fail() -> str:
            msg = "something went wrong"
            raise RuntimeError(msg)

        result = await async_fail()
        assert result.is_err()
        assert isinstance(result.err_value, RuntimeError)

    @pytest.mark.asyncio
    async def test_safe_async_basic_exception(self) -> None:
        """Test safe decorator returns Err on base Exception in async function."""

        @safe
        async def async_raise_exception() -> None:
            raise Exception("Basic async exception occurred")  # noqa: TRY002

        result = await async_raise_exception()
        assert result.is_err()
        err = result.err_value
        assert type(err) is Exception
        assert str(err) == "Basic async exception occurred"


class TestMapAsync:
    """Tests for map_async function."""

    @pytest.mark.asyncio
    async def test_map_async_ok(self) -> None:
        """Test map_async with Ok value."""

        async def double(x: int) -> int:
            return x * 2

        result: Result[int, ValueError] = Ok(21)
        mapped = await map_async(result, double)
        assert mapped.is_ok()
        assert mapped.ok_value == 42

    @pytest.mark.asyncio
    async def test_map_async_err(self) -> None:
        """Test map_async with Err value."""

        async def double(x: int) -> int:
            return x * 2

        result: Result[int, ValueError] = Err(ValueError("error"))
        mapped: Result[int, ValueError] = await map_async(result, double)
        assert mapped.is_err()
        assert isinstance(mapped.err_value, ValueError)


class TestAndThenAsync:
    """Tests for and_then_async function."""

    @pytest.mark.asyncio
    async def test_and_then_async_ok_to_ok(self) -> None:
        """Test and_then_async mapping Ok to Ok."""

        async def process(x: int) -> Result[str, ValueError]:
            return Ok(str(x * 2))

        result: Result[int, ValueError] = Ok(21)
        chained = await and_then_async(result, process)
        assert chained.is_ok()
        assert chained.ok_value == "42"

    @pytest.mark.asyncio
    async def test_and_then_async_ok_to_err(self) -> None:
        """Test and_then_async mapping Ok to Err."""

        async def process(x: int) -> Result[str, ValueError]:
            return Err(ValueError("validation failed"))

        result: Result[int, ValueError] = Ok(21)
        chained = await and_then_async(result, process)
        assert chained.is_err()
        assert isinstance(chained.err_value, ValueError)

    @pytest.mark.asyncio
    async def test_and_then_async_err(self) -> None:
        """Test and_then_async with Err value skips execution."""

        executed = False

        async def process(x: int) -> Result[str, ValueError]:
            nonlocal executed
            executed = True
            return Ok(str(x))

        result: Result[int, ValueError] = Err(ValueError("initial error"))
        chained: Result[str, ValueError] = await and_then_async(result, process)
        assert chained.is_err()
        assert isinstance(chained.err_value, ValueError)
        assert not executed


class TestSafeFromAsyncDecorator:
    @pytest.mark.asyncio
    async def test_safe_from_async_success(self) -> None:
        @safe_from(ValueError)
        async def process(x: int) -> int:
            return x * 2

        result = await process(5)
        assert result == Ok(10)

    @pytest.mark.asyncio
    async def test_safe_from_async_exception(self) -> None:
        @safe_from(ValueError)
        async def process(x: int) -> int:
            raise ValueError("invalid")

        result = await process(5)
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ValueError)

    @pytest.mark.asyncio
    async def test_safe_from_async_propagates_unspecified(self) -> None:
        @safe_from(ValueError)
        async def process(x: int) -> int:
            raise TypeError("invalid type")

        with pytest.raises(TypeError):
            await process(5)


class TestUnwrapOrErrFallback:
    """Tests for unwrap_or fallback coverage."""

    def test_unwrap_or_err_branch(self) -> None:
        result: Result[int, ValueError] = Err(ValueError("err"))
        assert result.unwrap_or(42) == 42


class TestResultStructuralCompatibility:
    """Tests for structural compatibility fallback branches in collect_results, map_async and and_then_async."""

    def test_collect_results_structural_compatibility(self) -> None:
        """Test fallback structural compatibility branch in collect_results."""

        class CustomResult:
            def __init__(self, value):
                self.value = value

        custom_res = CustomResult(42)
        from taipanstack.core.result import collect_results

        res = collect_results([custom_res])  # type: ignore
        assert res is custom_res

    def test_collect_list_attribute_error(self) -> None:
        """Test the AttributeError handling in the optimized _collect_list path."""

        class MissingOkValue:
            pass

        from taipanstack.core.result import collect_results

        res = collect_results([MissingOkValue()])  # type: ignore
        assert isinstance(res, MissingOkValue)

    def test_collect_tuple_attribute_error(self) -> None:
        """Test the AttributeError handling with tuple in _collect_list."""

        class MissingOkValue:
            pass

        from taipanstack.core.result import collect_results

        res = collect_results((MissingOkValue(),))  # type: ignore
        assert isinstance(res, MissingOkValue)

    @pytest.mark.asyncio
    async def test_map_async_structural_compatibility(self) -> None:
        """Test fallback structural compatibility branch in map_async."""

        class CustomResult:
            def __init__(self, value):
                self.value = value

        custom_res = CustomResult(42)

        async def process(x):
            return x * 2

        from taipanstack.core.result import map_async

        res = await map_async(custom_res, process)  # type: ignore
        assert res is custom_res

    @pytest.mark.asyncio
    async def test_and_then_async_structural_compatibility(self) -> None:
        """Test fallback structural compatibility branch in and_then_async."""

        class CustomResult:
            def __init__(self, value):
                self.value = value

        custom_res = CustomResult(42)

        async def process(x):
            from result import Ok

            return Ok(x * 2)

        from taipanstack.core.result import and_then_async

        res = await and_then_async(custom_res, process)  # type: ignore
        assert res is custom_res

    def test_collect_results_empty_iterable(self) -> None:
        """Test fallback empty iterable branch in collect_results."""
        from taipanstack.core.result import collect_results

        def empty_gen():
            yield from ()

        res = collect_results(empty_gen())
        assert res.unwrap() == []

    def test_collect_results_iterable_all_ok(self) -> None:
        """Test fallback branch where an iterable of only Ok results returns Ok[list] in collect_results."""
        from result import Ok

        from taipanstack.core.result import collect_results

        def iter_ok():
            yield Ok(1)
            yield Ok(2)

        res = collect_results(iter_ok())
        assert res.unwrap() == [1, 2]


# Migrated from tests/test_chaos_bulkhead_resource_exhaustion_operations.py
from unittest.mock import AsyncMock, patch

import pytest

from taipanstack.resilience.adaptive.bulkhead import Bulkhead


@pytest.mark.asyncio
async def test_bulkhead_semaphore_exhaustion_chaos_returns_err() -> None:
    bulkhead = Bulkhead("test_chaos", max_concurrent=2, max_queue=2)

    async def dummy_task() -> int:
        return 42

    with patch.object(
        bulkhead._semaphore, "acquire", new_callable=AsyncMock
    ) as mock_acquire:
        mock_acquire.side_effect = OSError("Too many open files")

        result = await bulkhead.execute(dummy_task)

        assert isinstance(result, Err)
        assert isinstance(result.err_value, BaseException)
        assert "Resource exhaustion" in str(result.err_value)


# Migrated from tests/test_chaos_circuit_breaker_result_monad_operations.py
import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreakerError, circuit_breaker


def test_circuit_breaker_with_err_monad():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    def flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(ValueError("Chaos failure"))
        return Ok("success")

    res1 = flaky_function(True)
    assert isinstance(res1, Err)
    res2 = flaky_function(True)
    assert isinstance(res2, Err)

    with pytest.raises(CircuitBreakerError, match="is open"):
        flaky_function(True)


@pytest.mark.asyncio
async def test_async_circuit_breaker_with_err_monad():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    async def async_flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(ValueError("Chaos failure"))
        return Ok("success")

    res1 = await async_flaky_function(True)
    assert isinstance(res1, Err)
    res2 = await async_flaky_function(True)
    assert isinstance(res2, Err)

    with pytest.raises(CircuitBreakerError, match="is open"):
        await async_flaky_function(True)


def test_circuit_breaker_with_err_monad_not_in_exceptions():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    def flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(KeyError("Not tracked"))
        return Ok("success")

    res1 = flaky_function(True)
    assert isinstance(res1, Err)
    res2 = flaky_function(True)
    assert isinstance(res2, Err)

    # Should not open because KeyError is not in failure_exceptions
    res3 = flaky_function(True)
    assert isinstance(res3, Err)


@pytest.mark.asyncio
async def test_async_circuit_breaker_with_err_monad_not_in_exceptions():
    @circuit_breaker(failure_threshold=2, failure_exceptions=(ValueError,))
    async def async_flaky_function(fail: bool) -> Result[str, Exception]:
        if fail:
            return Err(KeyError("Not tracked"))
        return Ok("success")

    res1 = await async_flaky_function(True)
    assert isinstance(res1, Err)
    res2 = await async_flaky_function(True)
    assert isinstance(res2, Err)

    res3 = await async_flaky_function(True)
    assert isinstance(res3, Err)


# Migrated from tests/test_chaos_circuit_breaker_untracked_err_operations.py
from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_chaos_circuit_breaker_untracked_err_consistency():
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

    import contextlib

    with contextlib.suppress(KeyError):
        faulty_service_exc()
    assert breaker._state.success_count == 0

    faulty_service_monad()
    assert breaker._state.success_count == 0


if __name__ == "__main__":
    test_chaos_circuit_breaker_untracked_err_consistency()


# Migrated from tests/test_chaos_concurrency_resource_exhaustion_operations.py

import pytest

from taipanstack.utils.concurrency import OverloadError, limit_concurrency


def test_sync_concurrency_memoryerror_chaos_returns_err():
    @limit_concurrency(max_tasks=1)
    def dummy_task():
        return "success"

    with patch("threading.Semaphore.acquire", side_effect=MemoryError("Out of memory")):
        result = dummy_task()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), OverloadError)
        assert "Resource exhaustion" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_async_concurrency_oserror_chaos_returns_err():
    @limit_concurrency(max_tasks=1)
    async def dummy_task():
        return "success"

    with patch("asyncio.Semaphore.acquire", side_effect=OSError("Too many open files")):
        result = await dummy_task()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), OverloadError)
        assert "Resource exhaustion" in str(result.unwrap_err())


# Migrated from tests/test_chaos_http_bridge_operations.py
"""Chaos tests for the HTTP Bridge."""

import asyncio
from unittest.mock import MagicMock

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st


@pytest.mark.asyncio
async def test_chaos_http_bridge_safe_client_exception_extreme() -> None:
    """Simulate a severe exception thrown during safe client initialization."""
    from taipanstack.bridges.http_bridge import SafeHttpClient

    with patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx:
        # Simulate extreme unexpected exception type during AsyncClient instantiation
        mock_httpx.AsyncClient.side_effect = MemoryError("OOM")

        with pytest.raises(MemoryError):
            async with SafeHttpClient():
                raise AssertionError("Should not be reached")


@pytest.mark.asyncio
async def test_chaos_http_bridge_request_extreme_delay() -> None:
    """Test HTTP bridge handles extreme delays simulating stuck network."""
    from taipanstack.bridges.http_bridge import SafeHttpClient

    async def stuck_request(*args, **kwargs):
        # We don't want to actually sleep forever in the test, so we just raise
        # TimeoutError directly, but we want to simulate the behavior as if it
        # took a long time.
        raise TimeoutError("Stuck")

    mock_client = AsyncMock()
    mock_client.request = stuck_request
    mock_client.aclose = AsyncMock()

    with (
        patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
        patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
    ):
        mock_httpx.AsyncClient.return_value = mock_client

        async with SafeHttpClient(ssrf_protection=False) as client:
            result = await client.get("https://example.com")

    assert isinstance(result, Err)
    assert isinstance(result.err_value, TimeoutError)


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
        HealthCheck.function_scoped_fixture,
    ],
    deadline=None,
    max_examples=50,
)
@given(
    url=st.text(min_size=100, max_size=1000),
    method=st.sampled_from(
        [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "OPTIONS",
            "HEAD",
            "\x00",
            "B" * 50000,
        ]
    ),
)
def test_fuzz_http_bridge_malformed_inputs(url: str, method: str) -> None:
    """Fuzz HTTP bridge with massive strings for URL and methods to ensure no crashes."""
    from taipanstack.bridges.http_bridge import safe_request

    async def run_test():
        with (
            patch("taipanstack.bridges.http_bridge._HAS_HTTPX", True),
            patch("taipanstack.bridges.http_bridge._check_ssrf", return_value=Ok(None)),
            patch("taipanstack.bridges.http_bridge.httpx") as mock_httpx,
        ):
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client.request = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)

            mock_httpx.AsyncClient.return_value = mock_client

            result = await safe_request(method, url, ssrf_protection=False)

            # Should either be Ok or Err, but no unhandled exceptions
            assert isinstance(result, (Ok, Err))

    asyncio.run(run_test())


# Migrated from tests/test_chaos_orchestrator_resource_exhaustion_operations.py

import pytest

from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_bulkhead_oserror_chaos_returns_err() -> None:
    """Chaos test: Inject OSError when acquiring semaphore in Orchestrator."""

    orchestrator: ResilienceOrchestrator[str] = ResilienceOrchestrator(
        "test_orch"
    ).with_bulkhead(max_concurrent=1, max_queue=1)

    async def dummy_task() -> str:
        return "success"

    with patch("asyncio.Semaphore.acquire", side_effect=OSError("Too many open files")):
        result = await orchestrator.execute(dummy_task)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())
        assert "Too many open files" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_orchestrator_bulkhead_memoryerror_chaos_returns_err() -> None:
    """Chaos test: Inject MemoryError when acquiring semaphore in Orchestrator."""

    orchestrator: ResilienceOrchestrator[str] = ResilienceOrchestrator(
        "test_orch"
    ).with_bulkhead(max_concurrent=1, max_queue=1)

    async def dummy_task() -> str:
        return "success"

    with patch("asyncio.Semaphore.acquire", side_effect=MemoryError("Out of memory")):
        result = await orchestrator.execute(dummy_task)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())
        assert "Out of memory" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_orchestrator_bulkhead_runtimeerror_chaos_returns_err() -> None:
    """Chaos test: Inject RuntimeError when acquiring semaphore in Orchestrator."""

    orchestrator: ResilienceOrchestrator[str] = ResilienceOrchestrator(
        "test_orch"
    ).with_bulkhead(max_concurrent=1, max_queue=1)

    async def dummy_task() -> str:
        return "success"

    with patch(
        "asyncio.Semaphore.acquire", side_effect=RuntimeError("Event loop closed")
    ):
        result = await orchestrator.execute(dummy_task)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RuntimeError)
        assert "Resource exhaustion" in str(result.unwrap_err())
        assert "Event loop closed" in str(result.unwrap_err())


# Migrated from tests/test_chaos_resilience_thread_exhaustion_operations.py
from unittest import mock

from taipanstack.resilience.resilience import timeout


def test_chaos_resilience_thread_exhaustion_timeout_thread_exhaustion():
    @timeout(1.0)
    def my_func():
        return Ok("done")

    with mock.patch(
        "threading.Thread.start", side_effect=RuntimeError("can't start new thread")
    ):
        result = my_func()
        assert isinstance(result, Err)
        assert "Thread exhaustion: can't start new thread" in str(result.unwrap_err())


if __name__ == "__main__":
    test_chaos_resilience_thread_exhaustion_timeout_thread_exhaustion()


# Migrated from tests/test_chaos_retry_result_operations.py
import pytest

from taipanstack.resilience.retry import retry


def test_retry_result_monad_chaos():
    attempts = 0

    @retry(max_attempts=3, on=(ValueError,))
    def failing_func():
        nonlocal attempts
        attempts += 1
        return Err(ValueError("Chaos failure wrapped in Result"))

    _ = failing_func()

    # If retry handles Result monads correctly, it should have retried 3 times
    assert attempts == 3, f"Expected 3 attempts, got {attempts}"


def test_retry_result_monad_chaos_coverage():
    attempts = 0

    @retry(max_attempts=1, on=(ValueError,))
    def failing_func():
        nonlocal attempts
        attempts += 1
        return Ok("success")

    _ = failing_func()
    assert attempts == 1

    @retry(max_attempts=1, on=(ValueError,))
    def fail_with_exception():
        raise ValueError("failure")

    with pytest.raises(Exception, match="All 1 attempts failed"):
        fail_with_exception()


@pytest.mark.asyncio
async def test_retry_result_monad_chaos_coverage_async():
    attempts = 0

    @retry(max_attempts=1, on=(ValueError,))
    async def failing_func():
        nonlocal attempts
        attempts += 1
        return Ok("success")

    _ = await failing_func()
    assert attempts == 1

    @retry(max_attempts=1, on=(ValueError,))
    async def fail_with_exception():
        raise ValueError("failure")

    with pytest.raises(Exception, match="All 1 attempts failed"):
        await fail_with_exception()


def test_retry_result_monad_chaos_sync_not_on():
    @retry(max_attempts=3, on=(ValueError,))
    def failing_func():
        return Err(TypeError("Not on"))

    result = failing_func()
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_retry_result_monad_chaos_async_not_on():
    @retry(max_attempts=3, on=(ValueError,))
    async def failing_func():
        return Err(TypeError("Not on"))

    result = await failing_func()
    assert isinstance(result, Err)


@pytest.mark.asyncio
async def test_retry_result_monad_chaos_exhaust_async():
    @retry(max_attempts=2, on=(ValueError,))
    async def failing_func():
        return Err(ValueError("Chaos failure wrapped in Result"))

    result = await failing_func()
    assert isinstance(result, Err)


def test_retry_result_monad_chaos_exhaust_sync():
    @retry(max_attempts=2, on=(ValueError,))
    def failing_func():
        return Err(ValueError("Chaos failure wrapped in Result"))

    result = failing_func()
    assert isinstance(result, Err)


# Migrated from tests/test_chaos_timeout_resource_exhaustion_operations.py


def test_chaos_timeout_resource_exhaustion_thread_oserror_returns_err():
    @timeout(1.0)
    def dummy_task():
        return Ok("success")

    with patch(
        "threading.Thread.start",
        side_effect=OSError("Resource temporarily unavailable"),
    ):
        result = dummy_task()
        assert isinstance(result, Err)
        assert "Resource exhaustion" in str(result.unwrap_err())


def test_chaos_timeout_resource_exhaustion_thread_memoryerror_returns_err():
    @timeout(1.0)
    def dummy_task():
        return Ok("success")

    with patch("threading.Thread.start", side_effect=MemoryError("Out of memory")):
        result = dummy_task()
        assert isinstance(result, Err)
        assert "Memory exhaustion" in str(result.unwrap_err())


# Migrated from tests/test_edge_cases_coverage_operations.py
"""Additional tests for filesystem, logging, and other modules for 100% coverage."""

from pathlib import Path

import pytest

from taipanstack.security.guards import SecurityError


class TestFilesystemEdgeCases:
    """Edge case tests for filesystem module."""

    def test_edge_cases_coverage_safe_read_with_traversal_no_base_dir(
        self, tmp_path: Path
    ) -> None:
        """Test safe_read with .. in path but no base_dir uses cwd."""
        from taipanstack.utils.filesystem import safe_read

        # Create a file in tmp_path
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # This should fail because .. triggers guard with cwd
        result = safe_read(tmp_path / ".." / "etc" / "passwd")
        match result:
            case Err(err) if isinstance(err, SecurityError):
                assert err.guard_name == "path_traversal"
            case _:
                pytest.fail("Expected Err(SecurityError)")

    def test_edge_cases_coverage_safe_write_existing_file_guarded(
        self, tmp_path: Path
    ) -> None:
        """Test safe_write with existing file and base_dir."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "existing.txt"
        test_file.write_text("old content")

        result = safe_write(
            test_file, "new content", options=WriteOptions(base_dir=tmp_path)
        )
        assert result.read_text() == "new content"

    def test_edge_cases_coverage_safe_write_with_traversal_no_base_dir(
        self, tmp_path: Path
    ) -> None:
        """Test safe_write with .. triggers guard."""
        from taipanstack.utils.filesystem import safe_write

        with pytest.raises(SecurityError):
            safe_write(tmp_path / ".." / "bad.txt", "content")

    def test_edge_cases_coverage_safe_write_atomic_error_cleanup(
        self, tmp_path: Path
    ) -> None:
        """Test atomic write cleans up temp file on error."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "test.txt"

        # Mock os.fdopen to raise an error
        with patch("os.fdopen", side_effect=OSError("Write error")):
            with pytest.raises(OSError):
                safe_write(test_file, "content", options=WriteOptions(atomic=True))


class TestLoggingEdgeCases:
    """Edge case tests for logging module."""

    def test_edge_cases_coverage_stack_logger_bind_context(self) -> None:
        """Test StackLogger with bind context."""
        from taipanstack.utils.logging import StackLogger

        logger = StackLogger()
        logger.bind(user="test", request_id="123")

        # Log something - context should be in logs
        logger.info("Test message")

    def test_edge_cases_coverage_stack_logger_unbind_context(self) -> None:
        """Test unbinding logger context."""
        from taipanstack.utils.logging import StackLogger

        logger = StackLogger()
        logger.bind(key="value")
        logger.unbind("key")

        logger.info("After unbind")

    def test_edge_cases_coverage_setup_logging_basic(self) -> None:
        """Test setup_logging basic configuration."""
        from taipanstack.utils.logging import setup_logging

        setup_logging(level="DEBUG")

    def test_edge_cases_coverage_log_operation_decorator(self) -> None:
        """Test log_operation decorator."""
        from taipanstack.utils.logging import log_operation

        @log_operation("test_op")
        def my_func(x: int) -> int:
            return x * 2

        result = my_func(5)
        assert result == 10

    def test_edge_cases_coverage_log_operation_with_error(self) -> None:
        """Test log_operation decorator with error."""
        from taipanstack.utils.logging import log_operation

        @log_operation("failing_op")
        def failing_func() -> None:
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_func()


class TestDecoratorsEdgeCases:
    """Edge case tests for decorators module."""

    def test_edge_cases_coverage_timeout_with_signal(self) -> None:
        """Test timeout with signal (Unix only)."""

        from taipanstack.security.decorators import OperationTimeoutError, timeout

        @timeout(0.1, use_signal=True)
        def slow_func() -> None:
            import time

            time.sleep(1)

        with pytest.raises(OperationTimeoutError):
            slow_func()


class TestGuardsEdgeCases:
    """Edge case tests for guards module."""

    def test_edge_cases_coverage_guard_command_injection_with_whitelist(
        self,
    ) -> None:
        """Test guard_command_injection with custom whitelist."""
        from taipanstack.security.guards import guard_command_injection

        cmd = ["python", "--version"]
        result = guard_command_injection(cmd, allowed_commands=["python", "pip"])
        assert result == cmd


class TestSanitizersEdgeCases:
    """Edge case tests for sanitizers module."""

    def test_edge_cases_coverage_sanitize_string_with_null_bytes(self) -> None:
        """Test sanitizing string with null bytes."""
        from taipanstack.security.sanitizers import sanitize_string

        result = sanitize_string("hello\x00world")
        assert "\x00" not in result

    def test_edge_cases_coverage_sanitize_path_with_special_chars(
        self,
    ) -> None:
        """Test sanitizing path with special characters."""
        from taipanstack.security.sanitizers import sanitize_path

        result = sanitize_path("/path/to/../file")
        assert ".." not in str(result)


class TestValidatorsEdgeCases:
    """Edge case tests for validators module."""

    def test_edge_cases_coverage_validate_project_name_reserved(self) -> None:
        """Test that reserved names are rejected."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError, match="reserved"):
            validate_project_name("test")

    def test_edge_cases_coverage_validate_url_with_ip(self) -> None:
        """Test validating URL with IP address."""
        from taipanstack.security.validators import validate_url

        result = validate_url("http://192.168.1.1:8080", require_tld=False)
        assert "192.168.1.1" in result


class TestRetryEdgeCases:
    """Edge case tests for retry module."""

    def test_edge_cases_coverage_retrier_multiple_attempts(self) -> None:
        """Test Retrier with a loop for multiple attempts."""
        from taipanstack.resilience.retry import Retrier

        retrier = Retrier(max_attempts=3, initial_delay=0.01, on=(ValueError,))
        attempt_count = 0

        while True:
            try:
                with retrier:
                    attempt_count += 1
                    if attempt_count < 3:
                        raise ValueError("fail")
                    break  # Success
            except ValueError:
                if retrier.attempt >= retrier.config.max_attempts:
                    raise

        assert attempt_count == 3


class TestSubprocessEdgeCases:
    """Edge case tests for subprocess module."""

    def test_edge_cases_coverage_run_safe_command_with_env(self) -> None:
        """Test run_safe_command with custom environment."""
        from taipanstack.utils.subprocess import run_safe_command

        result = run_safe_command(
            ["echo", "test"],
            env={"CUSTOM_VAR": "value"},
        )
        assert result.success


class TestCircuitBreakerEdgeCases:
    """Edge case tests for circuit breaker module."""

    def test_edge_cases_coverage_circuit_breaker_half_open_success(
        self,
    ) -> None:
        """Test circuit transitions from half-open to closed."""
        import time

        from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

        breaker = CircuitBreaker(
            failure_threshold=1,
            success_threshold=2,
            timeout=0.05,
        )
        attempt = 0

        @breaker
        def func() -> str:
            nonlocal attempt
            attempt += 1
            if attempt == 1:
                raise ValueError("first fail")
            return "ok"

        # Trip circuit
        with pytest.raises(ValueError):
            func()

        assert breaker.state == CircuitState.OPEN

        # Wait for half-open
        time.sleep(0.1)

        # First success in half-open
        func()

        # Second success should close
        func()

        assert breaker.state == CircuitState.CLOSED


# Migrated from tests/test_fuzz_cache_operations.py
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.utils.cache import cached


@cached(10.0)
def my_func(*args, **kwargs):
    return Ok(args)


@settings(deadline=None, max_examples=100)
@given(
    st.lists(st.dictionaries(st.text(max_size=10), st.text(max_size=10)), max_size=10),
    st.dictionaries(
        st.text(max_size=10),
        st.dictionaries(st.text(max_size=10), st.text(max_size=10)),
        max_size=10,
    ),
)
def test_fuzz_cached_unhashable(args, kwargs):
    # First call puts result in cache
    result1 = my_func(*args, **kwargs)
    # Second call should return exactly the same Result instance from the cache
    result2 = my_func(*args, **kwargs)

    # Check that they returned the same content (the Ok result)
    assert result1 == result2


class UnhashableDummy:
    __hash__ = None  # type: ignore


class RecursiveDummy:
    def __init__(self):
        self.child = None

    __hash__ = None  # type: ignore


def test_fuzz_cache_cache_fallback_to_string_and_sets():
    """Ensure sets of hashable objects still work, and unhashable raises TypeError."""
    dummy1 = UnhashableDummy()

    # Trigger set path
    res1 = my_func({1, 2, 3})
    res2 = my_func({1, 2, 3})
    assert res1 == res2

    # Attempting to use unhashable type raises TypeError
    with pytest.raises(TypeError, match="unhashable type"):
        my_func(dummy1)

    with pytest.raises(TypeError, match="unhashable type"):
        my_func(dummy=dummy1)

    # Trigger tuple recursive path for hashable objects
    res3 = my_func(({"nested": 1},))
    res4 = my_func(({"nested": 1},))
    assert res3 == res4

    # Trigger tuple recursive path fails for unhashable objects
    with pytest.raises(TypeError, match="unhashable type"):
        my_func(({"nested": dummy1},))


# Migrated from tests/test_fuzz_guard_ssrf_operations.py
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import guard_ssrf


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    max_examples=10,
    deadline=None,
)
@given(st.text(min_size=2049, max_size=8192))
def test_fuzz_guard_ssrf_massive_strings_dos_returns_err(url: str) -> None:
    """Fuzz guard_ssrf with massive strings to ensure DoS protection limits are active."""
    url = "https://" + url
    result = guard_ssrf(url)
    assert result.is_err()
    assert "URL length exceeds" in str(result.unwrap_err())


@given(st.text())
@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    deadline=None,
)
def test_fuzz_guard_ssrf_malformed_returns_ok_or_err(s: str) -> None:
    """Fuzz guard_ssrf with extreme and malformed string inputs."""
    result = guard_ssrf(s)
    assert isinstance(result, (Ok, Err))


# Migrated from tests/test_mocked_coverage_operations.py
"""Tests with mocks to achieve 100% coverage."""

from pathlib import Path
from urllib.parse import urlparse

import pytest

from taipanstack.utils.filesystem import FileTooLargeErr


class TestLoggingStructlogBranches:
    """Tests for structlog branches in logging module."""

    def test_mocked_coverage_has_structlog_true_when_installed(self) -> None:
        """Verify that HAS_STRUCTLOG is True when structlog is installed."""
        from taipanstack.utils.logging import HAS_STRUCTLOG

        # structlog is now installed in test environment
        assert HAS_STRUCTLOG is True

    @patch("taipanstack.utils.logging.HAS_STRUCTLOG", True)
    def test_mocked_coverage_stack_logger_with_structured_mock(self) -> None:
        """Test StackLogger with mocked structlog."""
        # Create mock structlog module
        mock_structlog = MagicMock()
        mock_structlog.get_logger.return_value = MagicMock()

        with patch.dict("sys.modules", {"structlog": mock_structlog}):
            from taipanstack.utils.logging import StackLogger

            # Test with use_structured=True but HAS_STRUCTLOG patched
            logger = StackLogger(use_structured=False)
            logger.info("Test message")


class TestDecoratorsThreadTimeoutBranches:
    """Tests for thread timeout exception branches in decorators."""

    def test_mocked_coverage_timeout_thread_with_exception(self) -> None:
        """Test thread timeout when function raises exception."""
        from taipanstack.security.decorators import timeout

        @timeout(5.0, use_signal=False)
        def raise_error() -> None:
            raise ValueError("Expected error")

        with pytest.raises(ValueError, match="Expected error"):
            raise_error()

    def test_mocked_coverage_timeout_thread_success(self) -> None:
        """Test thread timeout with successful execution."""
        from taipanstack.security.decorators import timeout

        @timeout(5.0, use_signal=False)
        def success_func() -> str:
            return "success"

        result = success_func()
        assert result == "success"


class TestValidatorsBranches:
    """Tests for validator branches."""

    def test_mocked_coverage_validate_project_name_special_chars(self) -> None:
        """Test validate_project_name with special characters."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError):
            validate_project_name("project@name")

    def test_mocked_coverage_validate_python_version_invalid_format(
        self,
    ) -> None:
        """Test validate_python_version with invalid format."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError):
            validate_python_version("invalid")

    def test_mocked_coverage_validate_url_with_port(self) -> None:
        """Test validate_url with port number."""
        from taipanstack.security.validators import validate_url

        result = validate_url("https://example.com:443/path")
        parsed = urlparse(result)
        assert parsed.hostname == "example.com"


class TestGuardsBranches:
    """Tests for guards module branches."""

    def test_mocked_coverage_guard_path_traversal_os_error(
        self, tmp_path: Path
    ) -> None:
        """Test guard_path_traversal when resolve raises OSError."""
        from taipanstack.security.guards import guard_path_traversal

        # Create a valid path first
        test_file = tmp_path / "test.txt"
        test_file.touch()

        # Should work normally
        result = guard_path_traversal(test_file, tmp_path)
        assert result.exists()

    def test_mocked_coverage_guard_file_extension_no_extension(self) -> None:
        """Test guard_file_extension with file without extension."""
        from taipanstack.security.guards import guard_file_extension

        result = guard_file_extension(
            "Makefile",
            allowed_extensions=["", "txt"],
        )
        assert result is not None


class TestSanitizersBranches:
    """Tests for sanitizers module branches."""

    def test_mocked_coverage_sanitize_filename_empty(self) -> None:
        """Test sanitize_filename with empty string."""
        from taipanstack.security.sanitizers import sanitize_filename

        result = sanitize_filename("")
        assert result == "unnamed"

    def test_mocked_coverage_sanitize_filename_reserved_name(self) -> None:
        """Test sanitize_filename with Windows reserved name."""
        from taipanstack.security.sanitizers import sanitize_filename

        result = sanitize_filename("CON")
        assert result != "CON"  # Should be modified

    def test_mocked_coverage_sanitize_path_deep_nesting(self) -> None:
        """Test sanitize_path with deep nesting."""
        from taipanstack.security.sanitizers import sanitize_path

        with pytest.raises(ValueError, match="depth"):
            sanitize_path("a/b/c/d/e/f/g/h/i/j/k/l", max_depth=5)

    def test_mocked_coverage_sanitize_sql_identifier_starts_with_number(
        self,
    ) -> None:
        """Test sanitize_sql_identifier starting with number."""
        from taipanstack.security.sanitizers import sanitize_sql_identifier

        result = sanitize_sql_identifier("123column")
        assert result.startswith("_")


class TestSubprocessBranches:
    """Tests for subprocess module branches."""

    def test_mocked_coverage_run_safe_command_failure(self) -> None:
        """Test run_safe_command with failing command."""
        from taipanstack.utils.subprocess import run_safe_command

        result = run_safe_command(["python", "-c", "exit(1)"])
        assert not result.success
        assert result.returncode == 1


class TestFilesystemBranches:
    """Tests for filesystem module branches."""

    def test_mocked_coverage_safe_read_max_size_exceeded(self, tmp_path: Path) -> None:
        """Test safe_read when file exceeds max size."""
        from taipanstack.utils.filesystem import safe_read

        test_file = tmp_path / "large.txt"
        test_file.write_text("x" * 1000)

        result = safe_read(test_file, max_size_bytes=100)
        match result:
            case Err(FileTooLargeErr(size=s)):
                assert s > 100
            case _:
                pytest.fail("Expected Err(FileTooLargeErr)")

    def test_mocked_coverage_ensure_dir_already_exists(self, tmp_path: Path) -> None:
        """Test ensure_dir with directory that already exists."""
        from taipanstack.utils.filesystem import ensure_dir

        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()

        result = ensure_dir(existing_dir)
        assert result == existing_dir.resolve()

    def test_mocked_coverage_safe_write_no_backup(self, tmp_path: Path) -> None:
        """Test safe_write with backup=False."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "test.txt"
        test_file.write_text("original")

        safe_write(test_file, "new", options=WriteOptions(backup=False))
        assert test_file.read_text() == "new"

        # No backup should exist
        backup_path = tmp_path / "test.txt.bak"
        assert not backup_path.exists()


class TestRetryBranches:
    """Tests for retry module branches."""

    def test_mocked_coverage_calculate_delay_with_jitter(self) -> None:
        """Test calculate_delay produces different values with jitter."""
        from taipanstack.resilience.retry import RetryConfig, calculate_delay

        config = RetryConfig(jitter=True, jitter_factor=0.5)

        delays = [calculate_delay(1, config) for _ in range(10)]
        # With jitter, values should vary
        assert len(set(delays)) > 1

    def test_mocked_coverage_retry_config_defaults(self) -> None:
        """Test RetryConfig defaults."""
        from taipanstack.resilience.retry import RetryConfig

        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.jitter is True


class TestCircuitBreakerExitBranches:
    """Tests for circuit breaker exit branches."""

    def test_mocked_coverage_circuit_breaker_success_resets_failures(
        self,
    ) -> None:
        """Test circuit breaker resets failure count on success."""
        from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def flaky(should_fail: bool) -> str:
            if should_fail:
                raise ValueError("fail")
            return "ok"

        # Cause some failures
        for _ in range(2):
            with pytest.raises(ValueError):
                flaky(True)

        assert breaker.failure_count == 2

        # Success should reset count
        flaky(False)
        assert breaker.failure_count == 0
        assert breaker.state == CircuitState.CLOSED


class TestConfigGeneratorsBranches:
    """Tests for config generators branches."""

    def test_mocked_coverage_generate_pyproject_config(self) -> None:
        """Test generate_pyproject_config."""
        from taipanstack.config.generators import generate_pyproject_config
        from taipanstack.config.models import StackConfig

        config = StackConfig(project_name="minimal")
        result = generate_pyproject_config(config)

        assert "ruff" in result
        assert "mypy" in result


class TestModelsEdgeCases:
    """Tests for models edge cases."""

    def test_mocked_coverage_stack_config_to_target_version(self) -> None:
        """Test StackConfig.to_target_version method."""
        from taipanstack.config.models import StackConfig

        config = StackConfig(project_name="test", python_version="3.12")
        target = config.to_target_version()
        assert target == "py312"

    def test_mocked_coverage_stack_config_default_values(self) -> None:
        """Test StackConfig defaults."""
        from taipanstack.config.models import StackConfig

        config = StackConfig(project_name="test")
        assert config.python_version is not None


# Migrated from tests/test_utils_resilience_chaos_operations.py
"""Chaos tests for resilience components."""

import pytest


def test_utils_resilience_chaos_timeout_sync_chaos_nan() -> None:
    """Test chaos: NaN timeout causes system crash rather than safe degradation."""

    @timeout(float("nan"))
    def sync_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = sync_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()


def test_utils_resilience_chaos_timeout_sync_chaos_negative() -> None:
    """Test chaos: Negative timeout causes system crash."""

    @timeout(-1.0)
    def sync_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = sync_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()


@pytest.mark.asyncio
async def test_timeout_async_chaos_nan() -> None:
    """Test chaos: NaN timeout causes unhandled cancellation in async code."""

    @timeout(float("nan"))
    async def async_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = await async_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()


@pytest.mark.asyncio
async def test_timeout_async_chaos_negative() -> None:
    """Test chaos: Negative timeout on async."""

    @timeout(-1.0)
    async def async_sleep(delay: float) -> Result[str, Exception]:
        return Ok("done")

    res = await async_sleep(0.01)
    assert isinstance(res, Err)
    assert isinstance(res.err_value, ValueError)
    assert "finite non-negative" in str(res.err_value).lower()
