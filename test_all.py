from taipanstack.utils.rate_limit import RateLimiter

class PoisonFloat(float):
    def __add__(self, other):
        raise RuntimeError("Poisoned + operator")
    def __sub__(self, other):
        raise RuntimeError("Poisoned - operator")
    def __mul__(self, other):
        raise RuntimeError("Poisoned * operator")
    def __truediv__(self, other):
        raise RuntimeError("Poisoned / operator")
    def __ge__(self, other):
        raise RuntimeError("Poisoned >= operator")
    def __lt__(self, other):
        raise RuntimeError("Poisoned < operator")

limiter = RateLimiter(10, 1.0)
limiter.capacity = PoisonFloat(10.0)

try:
    limiter._calculate_new_tokens(1.0)
    print("calc new handled")
except Exception as e:
    print("calc new crashed")
