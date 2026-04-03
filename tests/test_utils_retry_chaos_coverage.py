import secrets

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_retry_chaos_jitter_nan(monkeypatch) -> None:
    # Test line 133 -> 139 where math.isfinite(jitter_amount) is False
    config = RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=float("inf"))
    # The exponential backoff will give finite delay, but jitter_amount = delay * inf = inf
    # This should bypass the jitter block and go to line 139
    delay = calculate_delay(1, config)
    assert delay == 1.0


def test_retry_chaos_jitter_exception(monkeypatch) -> None:
    # Test lines 136-137 exception logging
    config = RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=0.1)

    # Monkeypatch secrets.SystemRandom.uniform to raise an Exception
    class FakeRandom:
        def uniform(self, a, b):
            raise ValueError("Simulated exception")

    monkeypatch.setattr(secrets, "SystemRandom", FakeRandom)

    delay = calculate_delay(1, config)
    assert delay == 1.0


def test_retry_chaos_delay_negative() -> None:
    # Test line 140 (delay < 0 -> return 0.0)
    config = RetryConfig(initial_delay=-10.0, jitter=False)
    delay = calculate_delay(1, config)
    assert delay == 0.0
