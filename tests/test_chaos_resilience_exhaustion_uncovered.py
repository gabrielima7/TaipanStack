from unittest.mock import patch

import pytest

from taipanstack.core.result import Ok
from taipanstack.resilience.resilience import timeout
from taipanstack.resilience.retry import Retrier


def test_retrier_sleep_exhaustion_keyboard_interrupt():
    retrier = Retrier(max_attempts=3, on=(ValueError,))
    with patch("time.sleep", side_effect=KeyboardInterrupt()):
        with pytest.raises(KeyboardInterrupt):
            with retrier:
                raise ValueError("Oops")


def test_retrier_sleep_exhaustion_generic():
    retrier = Retrier(max_attempts=3, on=(ValueError,))
    with patch("time.sleep", side_effect=Exception("mock sleep error")):
        with pytest.raises(ValueError):
            with retrier:
                raise ValueError("Oops")


@pytest.mark.asyncio
async def test_timeout_wait_for_keyboard_interrupt():
    @timeout(1.0)
    async def my_func():
        return Ok("success")

    async def mock_wait_for(coro, timeout=None):
        coro.close()
        raise KeyboardInterrupt()

    with patch("asyncio.wait_for", new=mock_wait_for):
        with pytest.raises(KeyboardInterrupt):
            await my_func()


@pytest.mark.asyncio
async def test_retry_async_sleep_keyboard_interrupt():
    from taipanstack.resilience.retry import retry

    @retry(max_attempts=3, initial_delay=0.1)
    async def my_func():
        raise ValueError("Oops")

    with patch("asyncio.sleep", side_effect=KeyboardInterrupt()):
        with pytest.raises(KeyboardInterrupt):
            await my_func()
