from taipanstack.utils.rate_limit import RateLimiter

class PoisonFloat(float):
    def __add__(self, other):
        raise RuntimeError("Poisoned + operator")

limiter = RateLimiter(10, 1.0)
limiter.tokens = PoisonFloat(5.0)

try:
    limiter._apply_new_tokens(2.0)
    print("Handled!")
except Exception as e:
    print("Crash!", repr(e))
