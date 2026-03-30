"""Tests for AdaptiveTimeout."""

import asyncio

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_timeout import (
    AdaptiveTimeout,
    AdaptiveTimeoutError,
)


class TestAdaptiveTimeout:
    """Tests for the adaptive timeout logic."""

    def test_initial_state(self) -> None:
        """Starts with initial timeout."""
        at = AdaptiveTimeout("test", initial_timeout=2.5)
        assert at.current_timeout == 2.5
        assert at.current_ema is None

    def test_record_latency_updates_ema_and_timeout(self) -> None:
        """Recording latency updates EMA and changes timeout."""
        at = AdaptiveTimeout(
            "test",
            tolerance_multiplier=2.0,
            ema_alpha=0.5,
        )
        at.record_latency(1.0)
        assert at.current_ema == 1.0
        # 1.0 * 2.0 = 2.0
        assert at.current_timeout == 2.0

        at.record_latency(0.5)
        # EMA = 0.5 * 0.5 + (1 - 0.5) * 1.0 = 0.25 + 0.5 = 0.75
        assert at.current_ema == 0.75
        # Timeout = 0.75 * 2.0 = 1.5
        assert at.current_timeout == 1.5

    def test_timeout_bounded_by_min_max(self) -> None:
        """Timeout stays within min and max bounds."""
        at = AdaptiveTimeout(
            "test",
            min_timeout=1.0,
            max_timeout=10.0,
            tolerance_multiplier=2.0,
            ema_alpha=1.0,
        )
        at.record_latency(0.1)
        # Timeout would be 0.2, but bounded to 1.0
        assert at.current_timeout == 1.0

        at.record_latency(20.0)
        # Timeout would be 40.0, but bounded to 10.0
        assert at.current_timeout == 10.0

    def test_evaluate_result_ok(self) -> None:
        """Evaluating Ok result updates latency."""
        at = AdaptiveTimeout(
            "test",
            min_timeout=0.1,
            max_timeout=5.0,
        )
        res = Ok(42)
        ret = at.evaluate_result(res, duration=1.5)
        assert ret is res
        assert at.current_ema == 1.5

    def test_evaluate_result_err(self) -> None:
        """Evaluating Err result does NOT update latency."""
        at = AdaptiveTimeout(
            "test",
            min_timeout=0.1,
            max_timeout=5.0,
        )
        res = Err(ValueError("bad"))
        ret = at.evaluate_result(res, duration=1.5)
        assert ret is res
        assert at.current_ema is None


class TestAdaptiveTimeoutWrapper:
    """Tests for the wrap decorator."""

    @pytest.mark.asyncio
    async def test_successful_call_updates_timeout(self) -> None:
        """Successful call updates the timeout dynamically."""
        at = AdaptiveTimeout(
            "test",
            initial_timeout=2.0,
            tolerance_multiplier=3.0,
            ema_alpha=1.0,
        )

        @at.wrap
        async def mock_call() -> Result[str, Exception]:
            await asyncio.sleep(0.1)
            return Ok("done")

        res = await mock_call()
        assert isinstance(res, Ok)
        assert res.ok_value == "done"

        # The new timeout should be approx 0.1 * 3 = 0.3
        assert at.current_timeout < 1.0
        assert at.current_timeout > 0.1

    @pytest.mark.asyncio
    async def test_timeout_exceeded_returns_err(self) -> None:
        """Call taking too long returns AdaptiveTimeoutError."""
        at = AdaptiveTimeout(
            "test",
            initial_timeout=0.05,
        )

        @at.wrap
        async def mock_call() -> Result[str, Exception]:
            await asyncio.sleep(0.2)
            return Ok("done")

        res = await mock_call()
        assert isinstance(res, Err)
        assert isinstance(res.err_value, AdaptiveTimeoutError)
        assert "Operation timed out" in str(res.err_value)

    @pytest.mark.asyncio
    async def test_function_raising_exception_returns_err(self) -> None:
        """Underlying exception is caught and returned as Err."""
        at = AdaptiveTimeout("test")

        @at.wrap
        async def mock_call() -> Result[str, Exception]:
            raise ValueError("boom")

        res = await mock_call()
        assert isinstance(res, Err)
        assert isinstance(res.err_value, ValueError)
