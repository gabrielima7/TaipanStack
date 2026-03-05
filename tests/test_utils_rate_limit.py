"""Tests for rate limiting utils."""

import pytest

from taipanstack.utils.rate_limit import RateLimiter, RateLimitError, rate_limit


class TestRateLimiter:
    """Tests for the RateLimiter token bucket."""

    def test_invalid_initialization(self) -> None:
        """Test invalid args to RateLimiter."""
        with pytest.raises(ValueError, match="must be > 0"):
            RateLimiter(0, 1.0)
        with pytest.raises(ValueError, match="must be > 0"):
            RateLimiter(10, -1.0)

    def test_consume_success(self) -> None:
        """Test consuming tokens successfully."""
        limiter = RateLimiter(max_calls=2, time_window=1.0)
        assert limiter.consume() is True
        assert limiter.consume() is True
        assert limiter.consume() is False

    def test_consume_refill(self, monkeypatch: pytest.MonkeyPatch) -> None:
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

    def test_sync_rate_limit(self) -> None:
        """Test rate limit applied to sync function."""

        @rate_limit(max_calls=2, time_window=10.0)
        def process() -> int:
            return 42

        res1 = process()
        assert res1.is_ok()
        assert res1.ok() == 42

        res2 = process()
        assert res2.is_ok()
        assert res2.ok() == 42

        res3 = process()
        assert res3.is_err()
        assert isinstance(res3.err(), RateLimitError)

    @pytest.mark.asyncio
    async def test_async_rate_limit(self) -> None:
        """Test rate limit applied to async function."""

        @rate_limit(max_calls=1, time_window=10.0)
        async def fetch_data() -> str:
            return "async data"

        res1 = await fetch_data()
        assert res1.is_ok()
        assert res1.ok() == "async data"

        res2 = await fetch_data()
        assert res2.is_err()
        assert isinstance(res2.err(), RateLimitError)
