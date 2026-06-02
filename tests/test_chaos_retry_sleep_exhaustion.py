from unittest.mock import patch

import pytest

from taipanstack.resilience.retry import Retrier, RetryError, retry


def test_chaos_retry_sync_sleep_oserror():
    attempts = 0

    @retry(max_attempts=3, on=(ValueError,), reraise=True)
    def flaky_func():
        nonlocal attempts
        attempts += 1
        raise ValueError("Oops")

    with patch("time.sleep", side_effect=OSError("System resource exhausted")):
        with pytest.raises((ValueError, RetryError)):
            flaky_func()

    assert attempts == 1


@pytest.mark.asyncio
async def test_chaos_retry_async_sleep_memoryerror():
    attempts = 0

    @retry(max_attempts=3, on=(ValueError,), reraise=True)
    async def flaky_func():
        nonlocal attempts
        attempts += 1
        raise ValueError("Oops")

    with patch("asyncio.sleep", side_effect=MemoryError("Out of memory")):
        with pytest.raises((ValueError, RetryError)):
            await flaky_func()

    assert attempts == 1


def test_chaos_retrier_sleep_exhaustion():
    retrier = Retrier(max_attempts=3, on=(ValueError,))
    attempts = 0

    with patch("time.sleep", side_effect=MemoryError("Out of memory")):
        with pytest.raises((ValueError, RetryError)):
            with retrier:
                attempts += 1
                raise ValueError("Oops")

    assert attempts == 1
