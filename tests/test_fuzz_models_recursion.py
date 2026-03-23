import json

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.models import _mask_data


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
def test_fuzz_mask_data_recursion(data):
    try:
        _mask_data(data)
    except RecursionError:
        pytest.fail("RecursionError raised!")


def test_deep_recursion_dict():
    data = {}
    current = data
    for _ in range(2000):
        current["nested"] = {}
        current = current["nested"]
    current["password"] = "secret"
    try:
        masked = _mask_data(data)

        # Verify it was masked or truncated
        dump = json.dumps(masked)
        assert "secret" not in dump, "Sensitive data was not masked or truncated"
    except RecursionError:
        pytest.fail("RecursionError raised!")


def test_deep_recursion_list():
    data = []
    current = data
    for _ in range(2000):
        new_list = []
        current.append(new_list)
        current = new_list
    current.append({"password": "secret"})
    try:
        masked = _mask_data(data)

        # Verify it was masked or truncated
        dump = json.dumps(masked)
        assert "secret" not in dump, "Sensitive data was not masked or truncated"
    except RecursionError:
        pytest.fail("RecursionError raised!")
