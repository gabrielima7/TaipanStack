import pytest

from taipanstack.resilience.resilience import timeout


def test_timeout_corrupt_float():
    class CorruptFloat(float):
        def __ge__(self, other):
            raise RuntimeError("Chaos __ge__")
        def __add__(self, other):
            raise RuntimeError("Chaos __add__")
        def __mul__(self, other):
            raise RuntimeError("Chaos __mul__")
        def __lt__(self, other):
            raise RuntimeError("Chaos __lt__")

    @timeout(CorruptFloat(1.0))
    def my_func():
        return 1

    try:
        result = my_func()
        # Verify it returns an Err because validation failed
        assert result.is_err()
    except Exception as e:
        pytest.fail(f"Timeout crashed with exception: {e}")
