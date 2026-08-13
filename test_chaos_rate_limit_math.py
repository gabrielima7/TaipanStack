from taipanstack.utils.rate_limit import RateLimiter
import time

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

limiter = RateLimiter(10, 1.0)
limiter.last_update = PoisonFloat(time.monotonic() - 0.5)

try:
    limiter.consume(1.0)
    print("last_update Handled!")
except Exception as e:
    print("last_update Crash!", repr(e))

limiter = RateLimiter(10, 1.0)
limiter.time_window = PoisonFloat(1.0)

try:
    limiter.consume(1.0)
    print("time_window Handled!")
except Exception as e:
    print("time_window Crash!", repr(e))

limiter = RateLimiter(10, 1.0)
limiter.capacity = PoisonFloat(10.0)

try:
    limiter.consume(1.0)
    print("capacity Handled!")
except Exception as e:
    print("capacity Crash!", repr(e))

limiter = RateLimiter(10, 1.0)
limiter.tokens = PoisonFloat(5.0)

try:
    limiter.consume(1.0)
    print("tokens Handled!")
except Exception as e:
    print("tokens Crash!", repr(e))
