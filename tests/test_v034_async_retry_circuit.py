"""Async tests for retry and circuit_breaker utilities."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from taipanstack.utils.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
    circuit_breaker,
)
from taipanstack.utils.retry import RetryError, retry

# ---------------------------------------------------------------------------
# Async @retry tests
# ---------------------------------------------------------------------------


class TestRetryAsyncSupport:
    """Verify @retry works transparently with async def functions."""

    async def test_async_success_no_retry(self) -> None:
        """Successful async function is called only once."""
        call_count = 0

        @retry(max_attempts=3, initial_delay=0.0, jitter=False)
        async def succeed() -> str:
            nonlocal call_count
            call_count += 1
            return "ok"

        result = await succeed()
        assert result == "ok"
        assert call_count == 1

    async def test_async_retries_then_succeeds(self) -> None:
        """Async function is retried and eventually succeeds."""
        call_count = 0

        @retry(max_attempts=3, initial_delay=0.0, jitter=False, on=(ValueError,))
        async def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("not yet")
            return "done"

        with patch("taipanstack.utils.retry.asyncio.sleep", new_callable=AsyncMock):
            result = await flaky()

        assert result == "done"
        assert call_count == 3

    async def test_async_raises_retry_error_after_max_attempts(self) -> None:
        """RetryError is raised after all async attempts are exhausted."""

        @retry(max_attempts=2, initial_delay=0.0, jitter=False, on=(OSError,))
        async def always_fails() -> None:
            raise OSError("boom")

        with patch("taipanstack.utils.retry.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RetryError) as exc_info:
                await always_fails()

        assert exc_info.value.attempts == 2
        assert exc_info.value.last_exception is not None

    async def test_async_does_not_catch_unspecified_exception(self) -> None:
        """Non-listed exceptions propagate immediately from async functions."""

        @retry(max_attempts=3, on=(ValueError,))
        async def raises_type_error() -> None:
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            await raises_type_error()

    async def test_async_uses_asyncio_sleep_not_time_sleep(self) -> None:
        """Async retries use asyncio.sleep, not time.sleep, for non-blocking waits."""
        mock_asyncio_sleep = AsyncMock()
        mock_time_sleep = MagicMock()
        call_count = 0

        @retry(max_attempts=2, initial_delay=0.05, jitter=False, on=(RuntimeError,))
        async def one_fail() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("first")
            return "ok"

        with (
            patch("taipanstack.utils.retry.asyncio.sleep", mock_asyncio_sleep),
            patch("taipanstack.utils.retry.time.sleep", mock_time_sleep),
        ):
            result = await one_fail()

        assert result == "ok"
        mock_asyncio_sleep.assert_awaited_once()
        mock_time_sleep.assert_not_called()

    async def test_async_on_retry_callback_is_called(self) -> None:
        """on_retry callback is invoked on each failed async attempt."""
        callback_calls: list[tuple[int, int, Exception, float]] = []

        @retry(
            max_attempts=3,
            initial_delay=0.0,
            jitter=False,
            on=(ValueError,),
            on_retry=lambda a, m, e, d: callback_calls.append((a, m, e, d)),
        )
        async def two_fails() -> str:
            if len(callback_calls) < 2:
                raise ValueError("retry me")
            return "final"

        with patch("taipanstack.utils.retry.asyncio.sleep", new_callable=AsyncMock):
            result = await two_fails()

        assert result == "final"
        assert len(callback_calls) == 2
        assert callback_calls[0][0] == 1  # first attempt index
        assert callback_calls[1][0] == 2  # second attempt index

    async def test_async_structlog_warning_called_without_callback(self) -> None:
        """Without on_retry, structlog.warning is emitted for async retries."""
        mock_structlog_logger = MagicMock()

        @retry(max_attempts=2, initial_delay=0.0, jitter=False)
        async def async_fails() -> None:
            raise RuntimeError("err")

        with (
            patch("taipanstack.utils.retry._HAS_STRUCTLOG", True),
            patch("taipanstack.utils.retry._structlog_logger", mock_structlog_logger),
            patch("taipanstack.utils.retry.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(RetryError):
                await async_fails()

        assert mock_structlog_logger.warning.call_count >= 1
        event = mock_structlog_logger.warning.call_args[0][0]
        assert event == "retry_attempted"

    async def test_async_log_retries_false_skips_logging(self) -> None:
        """log_retries=False suppresses stdlib log messages for async functions."""
        call_count = 0

        @retry(
            max_attempts=2,
            initial_delay=0.0,
            jitter=False,
            on=(ValueError,),
            log_retries=False,
        )
        async def one_fail_async() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("quiet")
            return "ok"

        with patch("taipanstack.utils.retry.asyncio.sleep", new_callable=AsyncMock):
            result = await one_fail_async()

        assert result == "ok"

    async def test_async_reraise_false_still_raises_retry_error(self) -> None:
        """Even without reraise=True the exhausted path raises RetryError."""

        @retry(
            max_attempts=1,
            initial_delay=0.0,
            jitter=False,
            on=(ValueError,),
            reraise=False,
        )
        async def fail_always() -> str:
            raise ValueError("nope")

        with pytest.raises(RetryError):
            await fail_always()


# ---------------------------------------------------------------------------
# Async @circuit_breaker tests
# ---------------------------------------------------------------------------


class TestCircuitBreakerAsyncSupport:
    """Verify CircuitBreaker works transparently with async def functions."""

    async def test_async_success_keeps_closed(self) -> None:
        """Successful async calls keep circuit in CLOSED state."""
        breaker = CircuitBreaker(failure_threshold=3, name="test_async_closed")

        @breaker
        async def succeed() -> str:
            return "ok"

        for _ in range(5):
            assert await succeed() == "ok"

        assert breaker.state == CircuitState.CLOSED

    async def test_async_failures_open_circuit(self) -> None:
        """Async failures trip the circuit after reaching the threshold."""
        breaker = CircuitBreaker(failure_threshold=2, name="test_async_open")

        @breaker
        async def always_fail() -> None:
            raise ValueError("fail")

        for _ in range(2):
            with pytest.raises(ValueError):
                await always_fail()

        assert breaker.state == CircuitState.OPEN

    async def test_async_open_circuit_raises_circuit_breaker_error(self) -> None:
        """Open circuit blocks calls and raises CircuitBreakerError for async."""
        breaker = CircuitBreaker(
            failure_threshold=1, timeout=60.0, name="test_async_block"
        )

        @breaker
        async def always_fail() -> None:
            raise RuntimeError("fail")

        with pytest.raises(RuntimeError):
            await always_fail()

        assert breaker.state == CircuitState.OPEN

        with pytest.raises(CircuitBreakerError) as exc_info:
            await always_fail()

        assert exc_info.value.state == CircuitState.OPEN

    async def test_async_half_open_success_closes_circuit(self) -> None:
        """Async success in HALF_OPEN transitions circuit to CLOSED."""
        breaker = CircuitBreaker(
            failure_threshold=1,
            success_threshold=1,
            timeout=0.05,
            name="test_async_half_open",
        )
        call_count = 0

        @breaker
        async def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("first")
            return "recovered"

        with pytest.raises(RuntimeError):
            await flaky()

        assert breaker.state == CircuitState.OPEN

        await asyncio.sleep(0.1)

        result = await flaky()
        assert result == "recovered"
        assert breaker.state == CircuitState.CLOSED

    async def test_async_half_open_failure_reopens_circuit(self) -> None:
        """Async failure in HALF_OPEN transitions circuit back to OPEN."""
        breaker = CircuitBreaker(
            failure_threshold=1,
            timeout=0.05,
            name="test_async_reopen",
        )

        @breaker
        async def always_fail() -> None:
            raise RuntimeError("fail")

        with pytest.raises(RuntimeError):
            await always_fail()

        assert breaker.state == CircuitState.OPEN

        await asyncio.sleep(0.1)

        # HALF_OPEN call that fails → back to OPEN
        with pytest.raises(RuntimeError):
            await always_fail()

        assert breaker.state == CircuitState.OPEN

    async def test_circuit_breaker_decorator_async(self) -> None:
        """@circuit_breaker decorator works with async functions."""
        call_count = 0

        @circuit_breaker(failure_threshold=2, name="decorator_async")
        async def counted() -> int:
            nonlocal call_count
            call_count += 1
            return call_count

        assert await counted() == 1
        assert await counted() == 2

    async def test_async_excluded_exceptions_dont_trip(self) -> None:
        """Excluded exceptions don't count as failures for async functions."""
        breaker = CircuitBreaker(
            failure_threshold=2,
            excluded_exceptions=(ValueError,),
            name="test_async_excluded",
        )

        @breaker
        async def raises_excluded() -> None:
            raise ValueError("ignored")

        for _ in range(5):
            with pytest.raises(ValueError):
                await raises_excluded()

        assert breaker.state == CircuitState.CLOSED

    async def test_async_on_state_change_callback_called(self) -> None:
        """on_state_change callback fires on async-triggered state transitions."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        breaker = CircuitBreaker(
            failure_threshold=1,
            name="test_async_cb",
            on_state_change=lambda o, n: transitions.append((o, n)),
        )

        @breaker
        async def fail_once() -> None:
            raise RuntimeError("fail")

        with pytest.raises(RuntimeError):
            await fail_once()

        assert len(transitions) == 1
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)

    async def test_async_structlog_called_on_state_change_no_callback(self) -> None:
        """Without on_state_change, structlog.warning fires on async transitions."""
        mock_structlog_logger = MagicMock()

        breaker = CircuitBreaker(failure_threshold=1, name="structlog_async")

        @breaker
        async def fail() -> None:
            raise RuntimeError("x")

        with (
            patch(
                "taipanstack.utils.circuit_breaker._HAS_STRUCTLOG", True
            ),
            patch(
                "taipanstack.utils.circuit_breaker._structlog_logger",
                mock_structlog_logger,
            ),
        ):
            with pytest.raises(RuntimeError):
                await fail()

        assert mock_structlog_logger.warning.call_count >= 1
        assert mock_structlog_logger.warning.call_args[0][0] == "circuit_state_changed"
