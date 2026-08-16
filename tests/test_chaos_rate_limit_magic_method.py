import time

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limit_last_update_magic_method_chaos():
    limiter = RateLimiter(10, 1.0)

    class EvilFloat(float):
        def __rsub__(self, other):
            raise RuntimeError("Chaos injected on subtraction!")

    limiter.last_update = EvilFloat(time.monotonic())
    assert limiter.consume() is False


def test_rate_limit_tokens_add_magic_method_chaos():
    limiter = RateLimiter(10, 1.0)

    class EvilFloat(float):
        def __iadd__(self, other):
            raise RuntimeError("Chaos injected on __iadd__!")

        def __add__(self, other):
            raise RuntimeError("Chaos injected on __add__!")

    limiter.tokens = EvilFloat(10.0)
    limiter.last_update = time.monotonic() - 1.0
    assert limiter.consume() is False


def test_rate_limit_time_window_magic_method_chaos():
    limiter = RateLimiter(10, 1.0)

    class EvilFloat(float):
        def __rtruediv__(self, other):
            raise RuntimeError("Chaos injected on __rtruediv__!")

    limiter.time_window = EvilFloat(1.0)
    limiter.last_update = time.monotonic() - 1.0
    assert limiter.consume() is False


def test_rate_limit_capacity_magic_method_chaos():
    limiter = RateLimiter(10, 1.0)

    class EvilFloat(float):
        def __truediv__(self, other):
            raise RuntimeError("Chaos injected on __truediv__!")

    limiter.capacity = EvilFloat(10.0)
    limiter.last_update = time.monotonic() - 1.0
    assert limiter.consume() is False
