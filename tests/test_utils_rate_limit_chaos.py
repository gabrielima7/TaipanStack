"""Chaos test for rate limiter race conditions."""

import threading
import time

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_chaos_race_condition() -> None:
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
