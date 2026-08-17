import time
from unittest.mock import patch

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.utils.rate_limit import RateLimiter, RateLimitError, rate_limit


def test_chaos_rate_limit_lock_mutation_expected():
    """Chaos test: Corrupt lock state."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)

    class BadLock:
        def acquire(self, timeout=-1):
            raise RuntimeError("Corrupted lock state")

        def release(self):
            return None

    limiter._lock = BadLock()

    assert limiter.consume() is False


def test_chaos_rate_limit_state_mutation_expected():
    """Chaos test: Corrupt state to None."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    limiter.tokens = None  # type: ignore

    assert limiter.consume() is False


@pytest.mark.asyncio
async def test_chaos_rate_limit_async_decorator_exception():
    """Chaos test: Decorator exception handling for async."""

    @rate_limit(max_calls=1, time_window=1.0)
    async def my_func():
        return "success"

    with patch(
        "taipanstack.utils.rate_limit.RateLimiter.consume",
        side_effect=RuntimeError("test"),
    ):
        res = await my_func()

    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)


def test_chaos_rate_limit_sync_decorator_exception_expected():
    """Chaos test: Decorator exception handling for sync."""

    @rate_limit(max_calls=1, time_window=1.0)
    def my_func():
        return "success"

    with patch(
        "taipanstack.utils.rate_limit.RateLimiter.consume",
        side_effect=RuntimeError("test"),
    ):
        res = my_func()

    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)


def test_chaos_rate_limit_time_mutation_expected():
    """Chaos test: Corrupt time to None or string."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    limiter.last_update = "invalid_time"  # type: ignore
    assert limiter.consume() is False

    limiter.last_update = float("inf")  # type: ignore
    assert limiter.consume() is False


def test_chaos_rate_limit_capacity_mutation_expected():
    """Chaos test: Corrupt capacity to None."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    limiter.capacity = "invalid"  # type: ignore
    assert limiter.consume() is False


def test_chaos_rate_limit_time_window_mutation_expected():
    """Chaos test: Corrupt time_window to None."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    limiter.time_window = "invalid"  # type: ignore
    assert limiter.consume() is False


def test_chaos_rate_limit_tokens_mutation_expected():
    """Chaos test: Corrupt requested tokens to None or inf."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    assert limiter.consume(tokens=None) is False  # type: ignore
    assert limiter.consume(tokens=float("inf")) is False


def test_chaos_rate_limit_consume_negative_tokens_expected():
    """Chaos test: Negative tokens consumption."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    assert limiter.consume(tokens=-5.0) is True


def test_chaos_rate_limit_current_time_exception_expected():
    """Chaos test: Exception in time.monotonic()."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    with patch("time.monotonic", side_effect=Exception("time failure")):
        assert limiter.consume() is False


def test_chaos_rate_limit_apply_new_tokens_mutation_expected():
    """Chaos test: Corrupt tokens and new_tokens in _apply_new_tokens."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    # Corrupting internal tokens
    limiter.tokens = "invalid"  # type: ignore
    assert limiter._apply_new_tokens(new_tokens=1.0) is False
    assert limiter.tokens == 10.0  # Resets to capacity

    # Valid tokens, corrupt new_tokens
    assert limiter._apply_new_tokens(new_tokens="invalid") is False  # type: ignore

    # Valid tokens and new_tokens, but result is inf
    limiter.tokens = 5.0
    assert limiter._apply_new_tokens(new_tokens=float("inf")) is False
    assert limiter.tokens == 10.0  # Resets to capacity


def test_chaos_rate_limit_try_consume_mutation_expected():
    """Chaos test: Corrupt tokens to string in _try_consume."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    limiter.tokens = "invalid"  # type: ignore
    assert limiter._try_consume(tokens=1.0) is False

    limiter.tokens = float("inf")  # type: ignore
    assert limiter._try_consume(tokens=1.0) is False
    assert limiter.tokens == 10.0  # Resets to capacity


def test_chaos_rate_limit_apply_new_tokens_success_expected():
    """Test successful token application up to capacity."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    limiter.tokens = 5.0
    assert limiter._apply_new_tokens(4.0) is True
    assert limiter.tokens == 9.0


def test_chaos_rate_limit_apply_new_tokens_cap_expected():
    """Test token application caps at capacity."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    limiter.tokens = 5.0
    assert limiter._apply_new_tokens(10.0) is True
    assert limiter.tokens == 10.0


def test_chaos_rate_limit_add_tokens_invalid_new_tokens_expected():
    """Test _add_tokens returns false if _calculate_new_tokens is None."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    # mock _calculate_new_tokens
    import types

    limiter._calculate_new_tokens = types.MethodType(
        lambda _self, _elapsed: None, limiter
    )
    assert limiter._add_tokens(time.monotonic()) is False


def test_chaos_rate_limit_try_consume_success_expected():
    """Test _try_consume success and failure."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    assert limiter._try_consume(tokens=5.0) is True
    assert limiter.tokens == 5.0
    assert limiter._try_consume(tokens=6.0) is False
    assert limiter.tokens == 5.0


def test_chaos_rate_limit_process_consumption_true_expected():
    """Test _process_consumption wrapper true path."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    assert limiter._process_consumption(tokens=1.0) is True


def test_chaos_rate_limit_validate_and_add_tokens_type_mutation_expected():
    """Test _validate_and_add_tokens bad type."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    assert limiter._validate_and_add_tokens("bad") is False  # type: ignore


def test_chaos_rate_limit_validate_and_add_tokens_infinite_expected():
    """Test _validate_and_add_tokens infinite."""
    limiter = RateLimiter(max_calls=10, time_window=1.0)
    assert limiter._validate_and_add_tokens(float("inf")) is True


@pytest.mark.asyncio
async def test_chaos_rate_limit_async_wrapper_limit_exceeded():
    """Test async wrapper returns Err on consume False."""

    @rate_limit(max_calls=1, time_window=1.0)
    async def my_func():
        return "success"

    with patch("taipanstack.utils.rate_limit.RateLimiter.consume", return_value=False):
        res = await my_func()

    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)


def test_chaos_rate_limit_sync_wrapper_limit_exceeded_expected():
    """Test sync wrapper returns Err on consume False."""

    @rate_limit(max_calls=1, time_window=1.0)
    def my_func():
        return "success"

    with patch("taipanstack.utils.rate_limit.RateLimiter.consume", return_value=False):
        res = my_func()

    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)


@pytest.mark.asyncio
async def test_chaos_rate_limit_async_wrapper_success():
    """Test async wrapper returns Ok on consume True."""

    @rate_limit(max_calls=1, time_window=1.0)
    async def my_func():
        return "success"

    res = await my_func()
    assert isinstance(res, Ok)


def test_chaos_rate_limit_sync_wrapper_success_expected():
    """Test sync wrapper returns Ok on consume True."""

    @rate_limit(max_calls=1, time_window=1.0)
    def my_func():
        return "success"

    res = my_func()
    assert isinstance(res, Ok)


def test_chaos_rate_limit_init_nan_expected():
    """Test init throws ValueError on NaN/Inf."""
    with pytest.raises(ValueError):
        RateLimiter(max_calls=float("nan"), time_window=1.0)  # type: ignore
    with pytest.raises(ValueError):
        RateLimiter(max_calls=10, time_window=float("inf"))  # type: ignore
    with pytest.raises(ValueError):
        RateLimiter(max_calls=-1, time_window=1.0)
    with pytest.raises(ValueError):
        RateLimiter(max_calls=10, time_window=-1.0)
