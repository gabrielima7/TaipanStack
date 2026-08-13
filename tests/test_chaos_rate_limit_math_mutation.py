from taipanstack.utils.rate_limit import RateLimiter


class PoisonFloat(float):
    def __ge__(self, other):
        raise RuntimeError("Poisoned >= operator")

    def __lt__(self, other):
        raise RuntimeError("Poisoned < operator")

    def __add__(self, other):
        raise RuntimeError("Poisoned + operator")

    def __sub__(self, other):
        raise RuntimeError("Poisoned - operator")

    def __mul__(self, other):
        raise RuntimeError("Poisoned * operator")

    def __truediv__(self, other):
        raise RuntimeError("Poisoned / operator")


def test_rate_limit_capacity_mutation():
    limiter = RateLimiter(10, 1.0)
    limiter.capacity = PoisonFloat(10.0)
    assert limiter.consume(1.0) is False


def test_rate_limit_tokens_mutation():
    limiter = RateLimiter(10, 1.0)
    limiter.tokens = PoisonFloat(5.0)
    assert limiter.consume(1.0) is False


def test_rate_limit_try_consume_mutation():
    limiter = RateLimiter(10, 1.0)
    limiter.tokens = PoisonFloat(10.0)
    assert limiter._try_consume(1.0) is False
