from taipanstack.utils.rate_limit import RateLimiter

class PoisonFloat(float):
    def __ge__(self, other):
        raise RuntimeError("Poisoned >= operator")
    def __add__(self, other):
        raise RuntimeError("Poisoned + operator")
    def __sub__(self, other):
        raise RuntimeError("Poisoned - operator")

limiter = RateLimiter(10, 1.0)
limiter.tokens = PoisonFloat(10.0)

try:
    limiter.consume(1.0)
    print("Handled!")
except Exception as e:
    print("Crash!", repr(e))
