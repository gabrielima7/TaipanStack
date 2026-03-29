from taipanstack.core.result import Ok
from taipanstack.utils.cache import cached


@cached(10.0)
def my_func(*args, **kwargs):
    return Ok(args)


class UnhashableDummy:
    __hash__ = None  # type: ignore


def test_cache_fallback_to_string_and_sets():
    """Ensure the custom fallback and sets are fully covered without hypothesis."""
    dummy1 = UnhashableDummy()

    # Trigger set path (line 60) and fallback exception (line 64-65)
    res1 = my_func({1, 2, 3}, dummy=dummy1)
    res2 = my_func({1, 2, 3}, dummy=dummy1)
    assert res1 == res2

    # Trigger tuple recursive path (line 54)
    res3 = my_func(({"nested": dummy1},), dummy=dummy1)
    res4 = my_func(({"nested": dummy1},), dummy=dummy1)
    assert res3 == res4
