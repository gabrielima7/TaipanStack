import pytest
from hypothesis import given, settings, strategies as st
from taipanstack.utils.cache import cached
from taipanstack.core.result import Ok

@cached(10.0)
def my_func(*args, **kwargs):
    return Ok(args)

@settings(deadline=None, max_examples=1000)
@given(st.lists(st.dictionaries(st.text(), st.text())), st.dictionaries(st.text(), st.dictionaries(st.text(), st.text())))
def test_fuzz_cached_unhashable(args, kwargs):
    # First call puts result in cache
    result1 = my_func(*args, **kwargs)
    # Second call should return exactly the same Result instance from the cache
    result2 = my_func(*args, **kwargs)

    # Check that they returned the same content (the Ok result)
    assert result1 == result2
