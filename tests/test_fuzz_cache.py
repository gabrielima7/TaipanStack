from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Ok
from taipanstack.utils.cache import cached


@cached(10.0)
def my_func(*args, **kwargs):
    return Ok(args)


@settings(deadline=None, max_examples=100)
@given(
    st.lists(st.dictionaries(st.text(max_size=10), st.text(max_size=10)), max_size=10),
    st.dictionaries(
        st.text(max_size=10),
        st.dictionaries(st.text(max_size=10), st.text(max_size=10)),
        max_size=10,
    ),
)
def test_fuzz_cached_unhashable(args, kwargs):
    # First call puts result in cache
    result1 = my_func(*args, **kwargs)
    # Second call should return exactly the same Result instance from the cache
    result2 = my_func(*args, **kwargs)

    # Check that they returned the same content (the Ok result)
    assert result1 == result2


class UnhashableDummy:
    __hash__ = None  # type: ignore


class RecursiveDummy:
    def __init__(self):
        self.child = None

    __hash__ = None  # type: ignore


def test_cache_fallback_to_string_and_sets():
    """Ensure the custom fallback and sets are fully covered."""
    dummy1 = UnhashableDummy()

    # Trigger set path (line 60) and fallback exception (line 64-65)
    res1 = my_func({1, 2, 3}, dummy=dummy1)
    res2 = my_func({1, 2, 3}, dummy=dummy1)
    assert res1 == res2

    # Trigger tuple recursive path (line 54)
    res3 = my_func(({"nested": dummy1},), dummy=dummy1)
    res4 = my_func(({"nested": dummy1},), dummy=dummy1)
    assert res3 == res4
