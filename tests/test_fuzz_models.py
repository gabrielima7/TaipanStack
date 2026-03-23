import pytest
from hypothesis import given, settings, strategies as st
from pydantic import BaseModel

from taipanstack.security.models import SecureBaseModel

# We will recursively build up nested json values
# and verify it survives infinite recursion or extreme nesting
def recursive_json(depth=0):
    if depth > 5:
        return st.text()
    return st.one_of(
        st.text(),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans(),
        st.none(),
        st.lists(st.deferred(lambda: recursive_json(depth + 1)), max_size=5),
        st.dictionaries(st.text(), st.deferred(lambda: recursive_json(depth + 1)), max_size=5)
    )

@given(data=recursive_json())
@settings(max_examples=100)
def test_fuzz_mask_data(data):
    from taipanstack.security.models import _mask_data
    _mask_data(data)
