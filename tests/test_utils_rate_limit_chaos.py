"""Chaos test for rate limiter race conditions."""

import threading
import time

import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_chaos_race_condition_expected() -> None:
    """Simulate a severe race condition in RateLimiter.consume.

    Multiple threads attempt to consume a token simultaneously. By adding
    an artificial context switch right after the token count check, we
    expose the lack of thread-safety in the token deduction.
    """

    class ChaosLimiter(RateLimiter):
        def consume(self) -> bool:
            now = 100.0
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
                time.sleep(0.01)
                self.tokens -= 1.0
                return True
            return False

    limiter = ChaosLimiter(1, 1000.0)
    limiter.tokens = 1.0
    limiter.last_update = 100.0
    successes = 0

    def worker() -> None:
        nonlocal successes
        if limiter.consume():
            successes += 1

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert successes == 1, (
        f"Expected 1 success, got {successes}. Limiter tokens: {limiter.tokens}"
    )
    assert limiter.tokens == 0.0, f"Expected 0.0 tokens left, got {limiter.tokens}"


def test_rate_limiter_chaos_backward_clock_jump_expected(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """Simulate a severe NTP anomaly/backward clock jump in RateLimiter.

    If `time.monotonic()` returns a value smaller than `self.last_update`
    due to a system anomaly, `elapsed` becomes negative. This can cause the
    token count to artificially decrease, leading to resource starvation
    where valid requests are incorrectly rate-limited.
    """
    limiter = RateLimiter(max_calls=5, time_window=10.0)
    assert limiter.consume() is True
    assert limiter.consume() is True
    limiter.last_update = 100.0
    limiter.tokens = 3.0

    def fake_monotonic_backward() -> float:
        return -900.0

    monkeypatch.setattr(time, "monotonic", fake_monotonic_backward)
    assert limiter.consume() is True, "Rate limiter failed due to backward clock jump"
    assert limiter.tokens >= 0.0, "Token count became negative due to clock jump"
