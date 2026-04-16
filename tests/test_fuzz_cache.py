import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Ok
from taipanstack.utils.cache import cached


@cached(10.0)
def my_func(*args, **kwargs):
    return Ok(args)

@settings(deadline=None, max_examples=100)
@given(st.lists(st.dictionaries(st.text(max_size=10), st.text(max_size=10)), max_size=10), st.dictionaries(st.text(max_size=10), st.dictionaries(st.text(max_size=10), st.text(max_size=10)), max_size=10))
def test_fuzz_cached_unhashable_expected(args, kwargs):
    result1 = my_func(*args, **kwargs)
    result2 = my_func(*args, **kwargs)
    assert result1 == result2

class UnhashableDummy:
    __hash__ = None

class RecursiveDummy:

    def __init__(self):
        self.child = None
    __hash__ = None

def test_cache_fallback_to_string_and_sets_expected():
    """Ensure sets of hashable objects still work, and unhashable raises TypeError."""
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
