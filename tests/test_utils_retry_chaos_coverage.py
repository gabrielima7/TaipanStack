import secrets

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_retry_chaos_jitter_nan_expected(monkeypatch) -> None:
    config = RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=float("inf"))
    delay = calculate_delay(1, config)
    assert delay == 1.0


def test_retry_chaos_jitter_exception(monkeypatch) -> None:
    config = RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=0.1)

    class FakeRandom:
        def uniform(self, a, b):
            raise ValueError("Simulated exception")

    monkeypatch.setattr(secrets, "SystemRandom", FakeRandom)
    delay = calculate_delay(1, config)
    assert delay == 1.0


def test_retry_chaos_delay_negative_expected() -> None:
    config = RetryConfig(initial_delay=-10.0, jitter=False)
    delay = calculate_delay(1, config)
    assert delay == 0.0
