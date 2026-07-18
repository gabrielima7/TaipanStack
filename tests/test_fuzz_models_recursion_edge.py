import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.models import _mask_data


def test_fuzz_models_recursion_edge():
    res = _mask_data("test", 101)
    assert res == "<MAX_DEPTH_REACHED>"

def recursive_json(depth=0):
    if depth > 100:
        return st.text()
    return st.one_of(
        st.text(),
        st.integers(),
        st.none(),
        st.lists(st.deferred(lambda: recursive_json(depth + 1)), max_size=2),
        st.dictionaries(
            st.text(), st.deferred(lambda: recursive_json(depth + 1)), max_size=2
        ),
    )

@given(data=recursive_json())
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_models_recursion_fuzz_mask_data_recursion_edge(data):
    try:
        _mask_data(data)
    except RecursionError:
        pytest.fail("RecursionError raised!")
