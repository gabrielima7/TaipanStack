from unittest.mock import patch

import pytest

from taipanstack.core.result import Err
from taipanstack.utils.rate_limit import RateLimitError, rate_limit


def test_sync_rate_limit_memoryerror_chaos():
    @rate_limit(max_calls=1, time_window=1.0)
    def dummy_task():
        return "success"

    with patch(
        "taipanstack.utils.rate_limit.RateLimiter.consume",
        side_effect=MemoryError("Out of memory"),
    ):
        result = dummy_task()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RateLimitError)
        assert "Resource exhaustion" in str(result.unwrap_err())


@pytest.mark.asyncio
async def test_async_rate_limit_oserror_chaos():
    @rate_limit(max_calls=1, time_window=1.0)
    async def dummy_task():
        return "success"

    with patch(
        "taipanstack.utils.rate_limit.RateLimiter.consume",
        side_effect=OSError("Too many open files"),
    ):
        result = await dummy_task()
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), RateLimitError)
        assert "Resource exhaustion" in str(result.unwrap_err())
