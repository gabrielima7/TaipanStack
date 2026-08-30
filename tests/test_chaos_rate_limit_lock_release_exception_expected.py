from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limit_lock_release_exception_expected() -> None:
    limiter = RateLimiter(10, 1.0)

    class BadLock:
        def acquire(self, timeout: float = -1) -> bool:
            return True

        def release(self) -> None:
            raise RuntimeError("Chaos release error")

    limiter._lock = BadLock()  # type: ignore[assignment]

    # Should safely degrade and not crash
    try:
        limiter.consume()
    except Exception as e:
        raise AssertionError(f"consume() crashed with {e}") from e
