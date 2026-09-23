"""Tests for RetryConfig resilience against chaotic type mutations."""

from taipanstack.resilience.retry import RetryConfig


def test_retry_chaos_evil_type() -> None:
    """Ensure RetryConfig falls back to default when supplied an evil float subclass."""

    class EvilFloat(float):
        def __float__(self) -> float:
            raise RuntimeError("Chaos __float__")

        def __ge__(self, other: object) -> bool:
            raise RuntimeError("Chaos __ge__")

        def __gt__(self, other: object) -> bool:
            raise RuntimeError("Chaos __gt__")

        def __lt__(self, other: object) -> bool:
            raise RuntimeError("Chaos __lt__")

    config = RetryConfig(initial_delay=EvilFloat(1.0))
    assert type(config.initial_delay) is float
    assert config.initial_delay == 1.0

    config_bool = RetryConfig(initial_delay=True)  # type: ignore[arg-type]
    assert type(config_bool.initial_delay) is float
    assert config_bool.initial_delay == 1.0
