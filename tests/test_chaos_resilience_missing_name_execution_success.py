import functools

import pytest

from taipanstack.core.result import Ok
from taipanstack.resilience.circuit_breaker import circuit_breaker
from taipanstack.resilience.retry import retry
from taipanstack.utils.cache import cached
from taipanstack.utils.rate_limit import rate_limit


def sync_func(x: int) -> int:
    return x


async def async_func(x: int) -> int:
    return x


def test_chaos_resilience_missing_name_sync_execution_success() -> None:
    partial_func = functools.partial(sync_func, 1)

    cb_func = circuit_breaker()(partial_func)
    assert cb_func() == 1

    retry_func = retry()(partial_func)
    assert retry_func() == 1

    cached_func = cached(ttl=1)(partial_func)
    assert cached_func() == 1

    rl_func = rate_limit(max_calls=1, time_window=1.0)(partial_func)
    assert rl_func() == Ok(1)


@pytest.mark.asyncio
async def test_chaos_resilience_missing_name_async_execution_success() -> None:
    partial_func = functools.partial(async_func, 1)

    cb_func = circuit_breaker()(partial_func)
    assert await cb_func() == 1

    retry_func = retry()(partial_func)
    assert await retry_func() == 1

    cached_func = cached(ttl=1)(partial_func)
    assert await cached_func() == 1

    rl_func = rate_limit(max_calls=1, time_window=1.0)(partial_func)
    assert await rl_func() == Ok(1)
