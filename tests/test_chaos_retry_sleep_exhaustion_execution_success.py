from unittest.mock import patch

import pytest

from taipanstack.resilience.retry import Retrier, retry


def test_chaos_retry_sync_sleep_oserror_execution_success():
    attempts = 0

    @retry(max_attempts=3, on=(ValueError,), reraise=True)
    def flaky_func():
        nonlocal attempts
        attempts += 1
        raise ValueError("Oops")

    with patch("time.sleep", side_effect=OSError("System resource exhausted")):
        with pytest.raises(OSError, match="System resource exhausted"):
            flaky_func()

    assert attempts == 1


@pytest.mark.asyncio
async def test_chaos_retry_async_sleep_memoryerror_execution_success():
    attempts = 0

    @retry(max_attempts=3, on=(ValueError,), reraise=True)
    async def flaky_func():
        nonlocal attempts
        attempts += 1
        raise ValueError("Oops")

    with patch("asyncio.sleep", side_effect=MemoryError("Out of memory")):
        with pytest.raises(MemoryError, match="Out of memory"):
            await flaky_func()

    assert attempts == 1


def test_chaos_retrier_sleep_exhaustion_execution_success():
    retrier = Retrier(max_attempts=3, on=(ValueError,))
    attempts = 0

    with patch("time.sleep", side_effect=MemoryError("Out of memory")):
        with pytest.raises(MemoryError, match="Out of memory"):
            with retrier:
                attempts += 1
                raise ValueError("Oops")

    assert attempts == 1
