from taipanstack.utils.rate_limit import RateLimiter


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_last_update_expected():
    limiter = RateLimiter(10, 10.0)

    # Mutate last_update to string
    object.__setattr__(limiter, "last_update", "10.0")

    # Should safely fail closed
    assert limiter.consume() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_capacity_expected():
    limiter = RateLimiter(10, 10.0)

    # Mutate capacity to string
    object.__setattr__(limiter, "capacity", "10")

    # Should safely fail closed
    assert limiter.consume() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_tokens():
    limiter = RateLimiter(10, 10.0)

    # Mutate tokens to string
    object.__setattr__(limiter, "tokens", "10")

    # Should safely fail closed
    assert limiter.consume() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_time_window_expected():
    limiter = RateLimiter(10, 10.0)

    # Mutate time_window to string
    object.__setattr__(limiter, "time_window", "10.0")

    # Should safely fail closed
    assert limiter.consume() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_now_consume_expected():
    limiter = RateLimiter(10, 10.0)

    # Mutate last_update to dict to hit TypeError in math.isfinite(now)
    # Wait, now is from time.monotonic(), so it's always float.
    # But self.tokens in `math.isfinite(self.tokens)` inside `_add_tokens` or `self.tokens >= tokens`
    # Let's test _is_valid_bucket_state type error
    object.__setattr__(limiter, "time_window", "string")
    assert limiter._is_valid_bucket_state() is False

    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "capacity", "string")
    assert limiter._is_valid_bucket_state() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_add_tokens():
    limiter = RateLimiter(10, 10.0)
    # Mutate tokens to hit math.isfinite(self.tokens) TypeError in _add_tokens
    object.__setattr__(limiter, "tokens", "string")
    assert limiter._add_tokens(10.0) is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_consume_now_expected():
    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "tokens", "string")
    # consume tries tokens >= tokens
    assert limiter.consume() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_consume_now_not_finite_expected():
    import math

    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "tokens", "string")

    import unittest.mock

    with unittest.mock.patch("time.monotonic", return_value=math.nan):
        # Hits math.isfinite(now) == False, then tries tokens >= tokens -> TypeError
        assert limiter.consume() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_new_tokens():
    limiter = RateLimiter(10, 10.0)
    assert limiter._apply_new_tokens("string") is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_now_exception_expected():
    import unittest.mock

    limiter = RateLimiter(10, 10.0)
    with unittest.mock.patch("time.monotonic", side_effect=RuntimeError("Time failed")):
        assert limiter.consume() is False


def test_chaos_rate_limit_type_mutation_rate_limit_survives_type_mutation_now_not_float_expected():
    import unittest.mock

    limiter = RateLimiter(10, 10.0)
    with unittest.mock.patch("time.monotonic", return_value="string"):
        assert limiter.consume() is False
