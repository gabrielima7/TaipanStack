"""Chaos test for extreme retry parameters."""

import math
import time

import pytest

from taipanstack.resilience.retry import RetryConfig, RetryError, calculate_delay, retry


def test_calculate_delay_massive_overflow() -> None:
    """Simulate a severe math OverflowError due to massive attempt counts.

    In chaotic situations or extremely long-running processes, if the attempt
    count grows extraordinarily large, standard Python float math (e.g. 2.0 ** 10000)
    will throw an OverflowError. The resilience module must safely cap this to
    max_delay rather than crashing the system.
    """
    config = RetryConfig(
        initial_delay=1.0,
        exponential_base=2.0,
        max_delay=60.0,
        jitter=False,
    )

    # 2.0 ** 10000 will trigger an OverflowError
    delay = calculate_delay(10000, config)
    assert math.isclose(delay, 60.0)


def test_retry_massive_attempts_end_to_end(monkeypatch: "pytest.MonkeyPatch") -> None:
    """Verify that the decorator fully survives extreme iteration counts."""
    # Defang sleep so the test runs instantly
    monkeypatch.setattr(time, "sleep", lambda _x: None)

    calls = 0

    @retry(max_attempts=2000, max_delay=60.0, log_retries=False)
    def failing_service() -> None:
        nonlocal calls
        calls += 1
        raise ValueError("Simulated persistent failure")

    with pytest.raises(RetryError, match="All 2000 attempts failed"):
        failing_service()

    assert calls == 2000
