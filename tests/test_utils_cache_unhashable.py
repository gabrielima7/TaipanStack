import pytest

from taipanstack.core.result import Ok
from taipanstack.utils.cache import cached


@cached(10.0)
def my_func(*args, **kwargs):
    return Ok(args)


class UnhashableDummy:
    __hash__ = None  # type: ignore


def test_cache_unhashable_raises_typeerror():
    """Ensure passing unhashable types directly raises a TypeError."""
    dummy1 = UnhashableDummy()

    # Trigger set path for hashable items still works
    res1 = my_func({1, 2, 3})
    res2 = my_func({1, 2, 3})
    assert res1 == res2

    # Passing an unhashable dummy object should raise TypeError directly
    with pytest.raises(TypeError, match="unhashable type"):
        my_func(dummy1)

    with pytest.raises(TypeError, match="unhashable type"):
        my_func(dummy=dummy1)

    # Trigger tuple recursive path still works for hashable nested contents
    res3 = my_func(({"nested": 1},))
    res4 = my_func(({"nested": 1},))
    assert res3 == res4

    # Trigger tuple recursive path fails for unhashable nested contents
    with pytest.raises(TypeError, match="unhashable type"):
        my_func(({"nested": dummy1},))
