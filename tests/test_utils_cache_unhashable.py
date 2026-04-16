import pytest

from taipanstack.core.result import Ok
from taipanstack.utils.cache import cached


@cached(10.0)
def my_func(*args, **kwargs):
    return Ok(args)


class UnhashableDummy:
    __hash__ = None


def test_cache_unhashable_raises_typeerror_expected():
    """Ensure passing unhashable types directly raises a TypeError."""
    dummy1 = UnhashableDummy()
    res1 = my_func({1, 2, 3})
    res2 = my_func({1, 2, 3})
    assert res1 == res2
    with pytest.raises(TypeError, match="unhashable type"):
        my_func(dummy1)
    with pytest.raises(TypeError, match="unhashable type"):
        my_func(dummy=dummy1)
    res3 = my_func(({"nested": 1},))
    res4 = my_func(({"nested": 1},))
    assert res3 == res4
    with pytest.raises(TypeError, match="unhashable type"):
        my_func(({"nested": dummy1},))
