import time

import pytest

from taipanstack.core.result import Err
from taipanstack.utils.rate_limit import RateLimiter, RateLimitError, rate_limit


def test_chaos_rate_limit_time_goes_backwards():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    assert limiter.consume() is True
    assert limiter.consume() is False
    limiter.last_update = time.monotonic() + 10.0
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_time_nan():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    assert limiter.consume() is True
    limiter.last_update = float("nan")
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_token_inf():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.tokens = float("inf")
    res = limiter.consume()
    assert isinstance(res, bool)
    limiter.tokens = 1.0
    assert limiter.consume() is True

def test_chaos_rate_limit_token_nan():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.tokens = float("nan")
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_time_window_type_mutation():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.time_window = "corrupted"
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_capacity_type_mutation():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.capacity = {"corrupt": "data"}
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_lock_exhaustion():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter._lock.acquire()
    def mock_process(*args, **kwargs):
        raise ValueError("Simulated Exception inside lock")
    limiter._process_consumption = mock_process
    limiter._lock.release()
    res = limiter.consume()
    assert res is False

def test_chaos_rate_limit_state_corruption():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.tokens = ["corrupt"]
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_time_window_nan():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.time_window = float("nan")
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_capacity_nan():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.capacity = float("nan")
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_token_type_string():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    res = limiter.consume("1.0")
    assert res is False

def test_chaos_rate_limit_token_type_negative():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    res = limiter.consume(-1.0)
    assert res is True

def test_chaos_rate_limit_token_amount_nan():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    res = limiter.consume(float("nan"))
    assert res is False

def test_chaos_rate_limit_initialization_nan():
    with pytest.raises(ValueError, match="must be finite numbers"):
        RateLimiter(max_calls=float("nan"), time_window=1.0)

    with pytest.raises(ValueError, match="must be finite numbers"):
        RateLimiter(max_calls=1, time_window=float("nan"))

def test_chaos_rate_limit_initialization_negative():
    with pytest.raises(ValueError, match="must be > 0.0"):
        RateLimiter(max_calls=-1, time_window=1.0)

    with pytest.raises(ValueError, match="must be > 0.0"):
        RateLimiter(max_calls=1, time_window=-1.0)

    with pytest.raises(ValueError, match="must be > 0.0"):
        RateLimiter(max_calls=0, time_window=1.0)

def test_chaos_rate_limit_validate_init_type_mutation():
    with pytest.raises(TypeError):
        RateLimiter(max_calls="1", time_window=1.0)

    with pytest.raises(TypeError):
        RateLimiter(max_calls=1, time_window="1.0")

def test_chaos_rate_limit_validate_init_params_mutation():
    with pytest.raises(ValueError, match="must be finite numbers"):
        RateLimiter(max_calls=float("inf"), time_window=1.0)

    with pytest.raises(ValueError, match="must be finite numbers"):
        RateLimiter(max_calls=1, time_window=float("inf"))

def test_chaos_rate_limit_elapsed_time_infinity():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_time():
        return float("inf")
    limiter._get_current_time = mock_time
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_validate_add_tokens_mutation():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_time():
        return "corrupted time"
    limiter._get_current_time = mock_time
    res = limiter.consume()
    assert isinstance(res, bool)

    def mock_time_nan():
        return float("nan")
    limiter._get_current_time = mock_time_nan
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_validate_add_tokens_null():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_time():
        return None
    limiter._get_current_time = mock_time
    res = limiter.consume()
    assert isinstance(res, bool)

    def mock_time_inf():
        return float("inf")
    limiter._get_current_time = mock_time_inf
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_calculate_new_tokens_mutation():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_calc_new(elapsed):
        return "corrupt string"
    limiter._calculate_new_tokens = mock_calc_new
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_calculate_new_tokens_corrupt():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_calc_new_tokens(*args, **kwargs):
        return None
    limiter._calculate_new_tokens = mock_calc_new_tokens
    def mock_elapsed(*args, **kwargs):
        return 1.0
    limiter._calculate_elapsed = mock_elapsed
    res = limiter.consume(1.0)
    assert res is False

def test_chaos_rate_limit_calculate_new_tokens_exception():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_calc_new_tokens(*args, **kwargs):
        raise RuntimeError("Simulated failure inside calculate_new_tokens")
    limiter._calculate_new_tokens = mock_calc_new_tokens
    res = limiter.consume(1.0)
    assert res is False

def test_chaos_rate_limit_add_tokens_corrupt_state():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.capacity = "corrupted"
    def mock_calc_elapsed(now):
        return 1.0
    limiter._calculate_elapsed = mock_calc_elapsed
    res = limiter.consume(1.0)
    assert res is False

def test_chaos_rate_limit_calculate_elapsed_corrupt():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_calc_elapsed(now):
        return None
    limiter._calculate_elapsed = mock_calc_elapsed
    res = limiter.consume(1.0)
    assert res is False

def test_chaos_rate_limit_process_consumption_exception():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    def mock_process_consumption(*args, **kwargs):
        raise RuntimeError("Simulated failure inside process_consumption")
    limiter._process_consumption = mock_process_consumption
    res = limiter.consume(1.0)
    assert res is False

def test_chaos_rate_limit_lock_exception():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    class MockLock:
        def __enter__(self):
            raise RuntimeError("Lock acquire failed")
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    limiter._lock = MockLock()
    res = limiter.consume(1.0)
    assert res is False

def test_chaos_rate_limit_exception():
    @rate_limit(max_calls=1, time_window=1.0)
    def failing_func():
        raise ValueError("Simulated failure")

    with pytest.raises(ValueError, match="Simulated failure"):
        failing_func()

@pytest.mark.asyncio
async def test_chaos_rate_limit_exception_async():
    @rate_limit(max_calls=1, time_window=1.0)
    async def failing_func():
        raise ValueError("Simulated failure")

    with pytest.raises(ValueError, match="Simulated failure"):
        await failing_func()

def test_chaos_rate_limit_decorator_exception():
    @rate_limit(max_calls=1, time_window=1.0)
    def my_func():
        return "success"

    orig_consume = RateLimiter.consume

    def mock_consume(*args, **kwargs):
        return False

    RateLimiter.consume = mock_consume

    res = my_func()
    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)

    RateLimiter.consume = orig_consume

@pytest.mark.asyncio
async def test_chaos_rate_limit_decorator_exception_async():
    @rate_limit(max_calls=1, time_window=1.0)
    async def my_func():
        return "success"

    orig_consume = RateLimiter.consume

    def mock_consume(*args, **kwargs):
        return False

    RateLimiter.consume = mock_consume

    res = await my_func()
    assert isinstance(res, Err)
    assert isinstance(res.unwrap_err(), RateLimitError)

    RateLimiter.consume = orig_consume

def test_chaos_rate_limit_decorator_success_exception():
    @rate_limit(max_calls=1, time_window=1.0)
    def my_func():
        raise RuntimeError("Fail func")

    with pytest.raises(RuntimeError):
        my_func()

@pytest.mark.asyncio
async def test_chaos_rate_limit_decorator_success_exception_async():
    @rate_limit(max_calls=1, time_window=1.0)
    async def my_func():
        raise RuntimeError("Fail func async")

    with pytest.raises(RuntimeError):
        await my_func()

def test_chaos_rate_limit_error_default():
    err = RateLimitError()
    assert str(err) == "Rate limit exceeded"

def test_chaos_rate_limit_error_custom():
    err = RateLimitError("Custom error")
    assert str(err) == "Custom error"

def test_chaos_rate_limit_last_update_type_mutation():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.last_update = "corrupted string"
    res = limiter.consume()
    assert isinstance(res, bool)

def test_chaos_rate_limit_try_consume_tokens_type_mutation():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.tokens = "corrupted string"
    res = limiter._try_consume(1.0)
    assert res is False

def test_chaos_rate_limit_get_current_time_exception():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    import time
    orig_mono = time.monotonic
    def mock_mono():
        raise RuntimeError("Simulated time exception")
    time.monotonic = mock_mono
    res = limiter.consume()
    assert isinstance(res, bool)
    time.monotonic = orig_mono


def test_chaos_rate_limit_try_consume_tokens_nan():
    limiter = RateLimiter(max_calls=1, time_window=1.0)
    limiter.tokens = float("nan")
    res = limiter._try_consume(1.0)
    assert res is False
