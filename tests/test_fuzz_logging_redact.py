from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.utils.logging import _redact_dict


@given(value=st.dictionaries(st.one_of(st.text(), st.integers(), st.floats(), st.none(), st.booleans(), st.dates(), st.datetimes()), st.one_of(st.text(), st.integers(), st.floats(), st.none(), st.booleans(), st.dates(), st.datetimes())))
@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_redact_dict_extreme_keys_expected(value):
    """Bombard _redact_dict with extreme, non-string keys to test resilience.

    Keys generated include None, integers, floats, booleans, dates, and datetimes.
    The function should gracefully skip non-string keys instead of raising a TypeError.
    """
    mutable_value = dict(value)
    _redact_dict(mutable_value)
