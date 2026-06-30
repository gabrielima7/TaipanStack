import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import sanitize_path


@given(
    path=st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_sanitize_path_malformed_input_standard_expected(path):
    with pytest.raises(TypeError, match="path must be a string or PathLike object, got"):
        sanitize_path(path)
