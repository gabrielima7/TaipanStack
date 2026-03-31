import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.utils.logging import _redact_dict


@given(
    value=st.dictionaries(
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.none(),
            st.booleans(),
            st.dates(),
            st.datetimes(),
        ),
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.none(),
            st.booleans(),
            st.dates(),
            st.datetimes(),
        ),
    )
)
@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_redact_dict_extreme_keys(value):
    """Bombard _redact_dict with extreme, non-string keys to test resilience.

    Keys generated include None, integers, floats, booleans, dates, and datetimes.
    The function should gracefully skip non-string keys instead of raising a TypeError.
    """
    # We need a copy because hypothesis strategies give us read-only views sometimes,
    # or we might mutate the input dict and break hypothesis' assumptions if not careful,
    # but _redact_dict takes a MutableMapping and mutates it in place.
    # Actually hypothesis gives new dicts for each example.
    mutable_value = dict(value)
    _redact_dict(mutable_value)
