
import pytest

from taipanstack.utils.rate_limit import RateLimiter


def test_rate_limiter_chaos_type_mutation():
    """Simulate severe state corruption via custom type mutations."""

    class CorruptFloat(float):
        def __ge__(self, other):
            raise RuntimeError("Chaos __ge__")

        def __sub__(self, other):
            raise RuntimeError("Chaos __sub__")

        def __rsub__(self, other):
            raise RuntimeError("Chaos __rsub__")

        def __add__(self, other):
            raise RuntimeError("Chaos __add__")

        def __radd__(self, other):
            raise RuntimeError("Chaos __radd__")

        def __mul__(self, other):
            raise RuntimeError("Chaos __mul__")

        def __rmul__(self, other):
            raise RuntimeError("Chaos __rmul__")

    limiter = RateLimiter(1, 10.0)
    limiter.last_update = CorruptFloat(100.0)

    # This should not raise an exception, but safely return False or handle it.
    try:
        result = limiter.consume()
        assert result in (True, False)
    except Exception as e:
        pytest.fail(f"RateLimiter crashed with exception: {e}")


def test_rate_limiter_chaos_type_mutation_new_tokens():
    class CorruptFloat(float):
        def __mul__(self, other):
            raise RuntimeError("Chaos __mul__")

    limiter = RateLimiter(1, 10.0)
    limiter._calculate_elapsed = lambda _now: CorruptFloat(10.0)
    try:
        result = limiter.consume()
        assert result in (True, False)
    except Exception as e:
        pytest.fail(f"RateLimiter crashed with exception: {e}")


def test_rate_limiter_chaos_type_mutation_apply_tokens():
    class CorruptFloat(float):
        def __add__(self, other):
            raise RuntimeError("Chaos __add__")

    limiter = RateLimiter(1, 10.0)
    limiter.tokens = CorruptFloat(0.0)
    try:
        result = limiter.consume()
        assert result in (True, False)
    except Exception as e:
        pytest.fail(f"RateLimiter crashed with exception: {e}")


def test_rate_limiter_chaos_type_mutation_try_consume():
    class CorruptFloat(float):
        def __ge__(self, other):
            raise RuntimeError("Chaos __ge__")

        def __sub__(self, other):
            raise RuntimeError("Chaos __sub__")

    limiter = RateLimiter(1, 10.0)
    limiter.tokens = CorruptFloat(1.0)
    limiter._validate_and_add_tokens = lambda _now: True
    try:
        result = limiter.consume()
        assert result in (True, False)
    except Exception as e:
        pytest.fail(f"RateLimiter crashed with exception: {e}")
