"""Tests for rate limiting utils."""

import pytest

from taipanstack.utils.rate_limit import RateLimiter, RateLimitError, rate_limit


class TestRateLimiter:
    def test_utils_rate_limit_chaos_inf_time_window_return(self) -> None:
        with pytest.raises(ValueError):
            RateLimiter(10, float("inf"))

    def test_utils_rate_limit_chaos_negative_time_window_return(self) -> None:
        with pytest.raises(ValueError):
            RateLimiter(10, -1.0)

    def test_utils_rate_limit_chaos_inf_capacity_return(self) -> None:
        with pytest.raises(ValueError):
            RateLimiter(float("inf"), 1.0)

    def test_utils_rate_limit_chaos_nan_capacity_return(self) -> None:
        with pytest.raises(ValueError):
            RateLimiter(float("nan"), 1.0)

    def test_utils_rate_limit_chaos_corrupted_bucket(self) -> None:
        limiter = RateLimiter(10, 1.0)
        limiter.time_window = 0.0
        assert not limiter.consume()

        limiter.time_window = float("nan")
        assert not limiter.consume()

        limiter = RateLimiter(10, 1.0)
        limiter.capacity = 0.0
        assert not limiter.consume()

        limiter.capacity = float("nan")
        assert not limiter.consume()

    def test_utils_rate_limit_chaos_nan_inf_time(self) -> None:
        limiter = RateLimiter(10, 1.0)
        limiter.tokens = 0
        assert not limiter._add_tokens(float("nan"))
        limiter2 = RateLimiter(10, 1.0)
        assert not limiter2._add_tokens(limiter2.last_update + float("inf"))

    def test_utils_rate_limit_chaos_consume_nan_now(self) -> None:
        import time

        limiter = RateLimiter(10, 1.0)
        old_mono = time.monotonic
        time.monotonic = lambda: float("nan")
        try:
            assert limiter.consume()
            limiter.tokens = 0
            assert not limiter.consume()
        finally:
            time.monotonic = old_mono

    def test_utils_rate_limit_chaos_consume_adds_tokens_corrupted_new_tokens(
        self,
    ) -> None:
        limiter = RateLimiter(10, 1.0)
        limiter.tokens = 0
        limiter.last_update = -1e308
        assert not limiter.consume()

    def test_utils_rate_limit_chaos_consume_adds_tokens_corrupted_tokens_sum(
        self,
    ) -> None:
        limiter = RateLimiter(10, 1.0)
        limiter.tokens = float("nan")
        assert not limiter.consume()
        assert limiter.tokens == limiter.capacity

    def test_utils_rate_limit_chaos_consume_zero_or_negative_tokens(self) -> None:
        limiter = RateLimiter(10, 1.0)
        assert limiter.consume(0.0)
        assert limiter.consume(-1.0)

    """Tests for the RateLimiter token bucket."""

    def test_utils_rate_limit_invalid_initialization(self) -> None:
        """Test invalid args to RateLimiter."""
        with pytest.raises(ValueError, match="must be > 0"):
            RateLimiter(0, 1.0)
        with pytest.raises(ValueError, match="must be > 0"):
            RateLimiter(10, -1.0)

    def test_utils_rate_limit_consume_success(self) -> None:
        """Test consuming tokens successfully."""
        limiter = RateLimiter(max_calls=2, time_window=1.0)
        assert limiter.consume() is True
        assert limiter.consume() is True
        assert limiter.consume() is False

    def test_utils_rate_limit_consume_refill(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test token refill logic."""
        import time

        mock_time = 100.0

        def fake_monotonic() -> float:
            return mock_time

        monkeypatch.setattr(time, "monotonic", fake_monotonic)

        limiter = RateLimiter(max_calls=1, time_window=1.0)
        assert limiter.consume() is True
        assert limiter.consume() is False

        # Advance time by 1 second to cause refill
        mock_time = 101.0
        assert limiter.consume() is True
        assert limiter.consume() is False

        # Advance time significantly to test cap
        mock_time = 200.0
        assert limiter.consume() is True
        assert limiter.consume() is False


class TestRateLimitDecorator:
    """Tests for the @rate_limit decorator."""

    def test_utils_rate_limit_sync_rate_limit(self) -> None:
        """Test rate limit applied to sync function."""

        @rate_limit(max_calls=2, time_window=10.0)
        def process() -> int:
            return 42

        res1 = process()
        assert res1.is_ok()
        assert res1.ok_value == 42

        res2 = process()
        assert res2.is_ok()
        assert res2.ok_value == 42

        res3 = process()
        assert res3.is_err()
        assert isinstance(res3.err_value, RateLimitError)

    @pytest.mark.asyncio
    async def test_async_rate_limit(self) -> None:
        """Test rate limit applied to async function."""

        @rate_limit(max_calls=1, time_window=10.0)
        async def fetch_data() -> str:
            return "async data"

        res1 = await fetch_data()
        assert res1.is_ok()
        assert res1.ok_value == "async data"

        res2 = await fetch_data()
        assert res2.is_err()
        assert isinstance(res2.err_value, RateLimitError)


# Migrated from tests/test_chaos_rate_limit_nan_operations.py
import pytest


def test_chaos_rate_limit_nan():
    # Micro-chaos on rate_limit.
    # What happens when RateLimiter gets nan max_calls?

    with pytest.raises(ValueError, match="finite numbers"):
        RateLimiter(max_calls=float("nan"), time_window=1.0)

    with pytest.raises(ValueError, match="finite numbers"):
        RateLimiter(max_calls=10, time_window=float("nan"))

    with pytest.raises(ValueError, match="finite numbers"):

        @rate_limit(max_calls=float("inf"), time_window=1.0)
        def my_func():
            return None

        my_func()


# Migrated from tests/test_chaos_rate_limit_state_corruption_operations.py


def test_chaos_rate_limit_state_corruption_returns_false():
    """Simulate extreme state corruption in RateLimiter.

    If memory or state gets corrupted such that `time_window` is 0.0,
    the limiter should gracefully reject (fail closed) rather than crash
    with a ZeroDivisionError. Similarly, NaN and Inf capacities should be
    rejected safely.
    """
    limiter = RateLimiter(10, 10.0)

    # Chaos: Corrupt time_window to 0.0
    object.__setattr__(limiter, "time_window", 0.0)
    assert limiter.consume() is False

    # Chaos: Corrupt time_window to NaN
    object.__setattr__(limiter, "time_window", float("nan"))
    assert limiter.consume() is False

    # Chaos: Corrupt capacity to NaN
    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "capacity", float("nan"))
    assert limiter.consume() is False

    # Chaos: Corrupt capacity to Inf
    object.__setattr__(limiter, "capacity", float("inf"))
    assert limiter.consume() is False

    # Chaos: Corrupt tokens to NaN
    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "tokens", float("nan"))
    assert limiter.consume() is False


# Migrated from tests/test_chaos_rate_limit_tokens_mutation_operations.py
import math


def test_rate_limit_survives_type_mutation_tokens_arg() -> None:
    limiter = RateLimiter(10, 10.0)

    # Should safely fail closed when given invalid token types
    assert limiter.consume("string") is False  # type: ignore
    assert limiter.consume(None) is False  # type: ignore
    assert limiter.consume(object()) is False  # type: ignore

    # Should safely fail closed when given nan
    assert limiter.consume(math.nan) is False


# Migrated from tests/test_chaos_rate_limit_type_mutation.py


def test_rate_limit_survives_type_mutation_last_update():
    limiter = RateLimiter(10, 10.0)

    # Mutate last_update to string
    object.__setattr__(limiter, "last_update", "10.0")

    # Should safely fail closed
    assert limiter.consume() is False


def test_rate_limit_survives_type_mutation_capacity():
    limiter = RateLimiter(10, 10.0)

    # Mutate capacity to string
    object.__setattr__(limiter, "capacity", "10")

    # Should safely fail closed
    assert limiter.consume() is False


def test_rate_limit_survives_type_mutation_tokens():
    limiter = RateLimiter(10, 10.0)

    # Mutate tokens to string
    object.__setattr__(limiter, "tokens", "10")

    # Should safely fail closed
    assert limiter.consume() is False


def test_rate_limit_survives_type_mutation_time_window():
    limiter = RateLimiter(10, 10.0)

    # Mutate time_window to string
    object.__setattr__(limiter, "time_window", "10.0")

    # Should safely fail closed
    assert limiter.consume() is False


def test_rate_limit_survives_type_mutation_now_consume():
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


def test_rate_limit_survives_type_mutation_add_tokens():
    limiter = RateLimiter(10, 10.0)
    # Mutate tokens to hit math.isfinite(self.tokens) TypeError in _add_tokens
    object.__setattr__(limiter, "tokens", "string")
    assert limiter._add_tokens(10.0) is False


def test_rate_limit_survives_type_mutation_consume_now():
    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "tokens", "string")
    # consume tries tokens >= tokens
    assert limiter.consume() is False


def test_rate_limit_survives_type_mutation_consume_now_not_finite():
    import math

    limiter = RateLimiter(10, 10.0)
    object.__setattr__(limiter, "tokens", "string")

    import unittest.mock

    with unittest.mock.patch("time.monotonic", return_value=math.nan):
        # Hits math.isfinite(now) == False, then tries tokens >= tokens -> TypeError
        assert limiter.consume() is False


# Migrated from tests/test_chaos_rl_nan_operations.py
import time

import pytest


def test_chaos_rl_nan_rate_limiter_chaos_time_corruption(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)

    # Empty the bucket
    for _ in range(5):
        assert limiter.consume() is True
    assert limiter.consume() is False

    # Simulate time corruption (NaN)
    monkeypatch.setattr(time, "monotonic", lambda: math.nan)
    assert limiter.consume() is False

    # Restore normal time, fast forward 20 seconds
    # Bucket should normally refill
    monkeypatch.setattr(time, "monotonic", lambda: limiter.last_update + 20.0)

    # If vulnerable, last_update is poisoned with NaN, elapsed becomes NaN,
    # and max(0.0, NaN) is 0.0, so tokens never refill.
    assert limiter.consume() is True, "Rate limiter permanently poisoned by NaN time"


def test_chaos_rl_nan_rate_limiter_chaos_time_corruption_has_tokens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)

    # Do not empty the bucket, so it has tokens
    assert limiter.consume() is True
    assert limiter.tokens >= 1.0

    # Simulate time corruption (NaN)
    monkeypatch.setattr(time, "monotonic", lambda: math.nan)

    # Calling consume while time is NaN but bucket has tokens should succeed and deduct a token
    initial_tokens = limiter.tokens
    assert limiter.consume() is True
    assert limiter.tokens == initial_tokens - 1.0


def test_chaos_rl_nan_rate_limiter_chaos_consume_zero_tokens() -> None:
    limiter = RateLimiter(max_calls=5, time_window=10.0)
    assert limiter.consume(tokens=0) is True
    assert limiter.consume(tokens=-1) is True


# Migrated from tests/test_utils_rate_limit_chaos_operations.py
"""Chaos test for rate limiter race conditions."""

import threading

import pytest


def test_utils_rate_limit_chaos_rate_limiter_chaos_race_condition() -> None:
    """Simulate a severe race condition in RateLimiter.consume.

    Multiple threads attempt to consume a token simultaneously. By adding
    an artificial context switch right after the token count check, we
    expose the lack of thread-safety in the token deduction.
    """

    class ChaosLimiter(RateLimiter):
        def consume(self) -> bool:
            now = (
                100.0  # Static time to avoid actual time-based refills during the test
            )

            # The lock is added in the base class later, we simulate race in the original logic
            if hasattr(self, "_lock"):
                with self._lock:
                    return self._vulnerable_consume(now)
            else:
                return self._vulnerable_consume(now)

        def _vulnerable_consume(self, now: float) -> bool:
            elapsed = now - self.last_update
            self.last_update = now

            self.tokens += elapsed * (self.capacity / self.time_window)
            self.tokens = min(self.tokens, self.capacity)

            if self.tokens >= 1.0:
                time.sleep(0.01)  # Force context switch to simulate race condition
                self.tokens -= 1.0
                return True
            return False

    # Create a limiter that allows strictly 1 call per 1000 seconds
    limiter = ChaosLimiter(1, 1000.0)
    limiter.tokens = 1.0  # Start with 1 token
    limiter.last_update = 100.0

    successes = 0

    def worker() -> None:
        nonlocal successes
        if limiter.consume():
            successes += 1

    # Launch 10 threads simultaneously
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # The rate limiter MUST only allow 1 success, regardless of thread interleaving
    assert successes == 1, (
        f"Expected 1 success, got {successes}. Limiter tokens: {limiter.tokens}"
    )
    assert limiter.tokens == 0.0, f"Expected 0.0 tokens left, got {limiter.tokens}"


def test_utils_rate_limit_chaos_rate_limiter_chaos_backward_clock_jump(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """Simulate a severe NTP anomaly/backward clock jump in RateLimiter.

    If `time.monotonic()` returns a value smaller than `self.last_update`
    due to a system anomaly, `elapsed` becomes negative. This can cause the
    token count to artificially decrease, leading to resource starvation
    where valid requests are incorrectly rate-limited.
    """

    # Create a limiter allowing 5 calls per 10 seconds
    limiter = RateLimiter(max_calls=5, time_window=10.0)

    # Consume 2 tokens normally
    assert limiter.consume() is True
    assert limiter.consume() is True

    # We should have exactly 3.0 tokens left (since no time has passed yet)
    # Give it a tiny bit of time to avoid floating point issues
    limiter.last_update = 100.0
    limiter.tokens = 3.0

    # Simulate an NTP backward clock jump (time goes backwards by 1000 seconds)
    def fake_monotonic_backward() -> float:
        return -900.0  # 100 - 1000 = -900

    monkeypatch.setattr(time, "monotonic", fake_monotonic_backward)

    # Attempt to consume a token during the clock anomaly
    # If vulnerable, elapsed = -1000.0, tokens will become -497.0
    # and the consume will fail even though it should succeed
    assert limiter.consume() is True, "Rate limiter failed due to backward clock jump"
    assert limiter.tokens >= 0.0, "Token count became negative due to clock jump"
