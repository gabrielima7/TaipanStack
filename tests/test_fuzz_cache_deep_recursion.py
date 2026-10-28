import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.utils.cache import _make_hashable


def recursive_data(depth=0):
    if depth > 60:
        return st.text()
    return st.one_of(
        st.text(),
        st.integers(),
        st.lists(st.deferred(lambda: recursive_data(depth + 1)), max_size=2),
        st.dictionaries(
            st.text(), st.deferred(lambda: recursive_data(depth + 1)), max_size=2
        ),
    )


@given(recursive_data())
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_cache_deep_recursion_make_hashable_fuzzing(data):
    try:
        _make_hashable(data)
    except ValueError as e:
        assert "Cache key too deeply nested" in str(e)
    except RecursionError:
        pytest.fail("RecursionError raised during fuzzing!")


def test_fuzz_cache_deep_recursion_deep_list():
    # Force max depth
    data = []
    current = data
    for _ in range(2000):
        new_list = []
        current.append(new_list)
        current = new_list

    try:
        _make_hashable(data)
        pytest.fail("Should have raised ValueError")
    except ValueError as e:
        assert "Cache key too deeply nested" in str(e)


def test_fuzz_cache_deep_recursion_deep_dict():
    # Force max depth
    data = {}
    current = data
    for i in range(2000):
        new_dict = {}
        current[f"key_{i}"] = new_dict
        current = new_dict

    try:
        _make_hashable(data)
        pytest.fail("Should have raised ValueError")
    except ValueError as e:
        assert "Cache key too deeply nested" in str(e)
