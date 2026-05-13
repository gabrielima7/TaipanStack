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
