import secrets

from taipanstack.resilience.retry import RetryConfig, calculate_delay


def test_utils_retry_chaos_coverage_retry_chaos_jitter_nan_standard_expected(
    monkeypatch,
) -> None:
    import pytest

    # Test line 133 -> 139 where math.isfinite(jitter_amount) is False
    with pytest.raises(ValueError, match="finite"):
        RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=float("inf"))


def test_utils_retry_chaos_coverage_retry_chaos_jitter_exception_standard_expected(
    monkeypatch,
) -> None:
    # Test lines 136-137 exception logging
    config = RetryConfig(initial_delay=1.0, jitter=True, jitter_factor=0.1)

    # Monkeypatch secrets.SystemRandom.uniform to raise an Exception
    class FakeRandom:
        def uniform(self, a, b):
            raise ValueError("Simulated exception")

    monkeypatch.setattr(secrets, "SystemRandom", FakeRandom)

    delay = calculate_delay(1, config)
    assert delay == 1.0


def test_utils_retry_chaos_coverage_retry_chaos_delay_negative_standard_expected() -> (
    None
):
    # Test line 140 (delay < 0 -> return 0.0)
    config = RetryConfig(initial_delay=-10.0, jitter=False)
    delay = calculate_delay(1, config)
    assert delay == 0.0


def test_utils_retry_chaos_coverage_retry_chaos_jitter_nan_2_standard_expected(
    monkeypatch,
) -> None:
    # Test line 134 -> 140 where math.isfinite(jitter_amount) is False
    config = RetryConfig(initial_delay=1.0, jitter=True)
    object.__setattr__(config, "jitter_factor", float("inf"))
    delay = calculate_delay(1, config)
    assert delay == 1.0
