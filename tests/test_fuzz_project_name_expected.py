import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_project_name


@given(
    max_length=st.one_of(
        st.none(),
        st.booleans(),
        st.floats(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_project_name_malformed_max_length_expected(
    max_length,
) -> None:
    """Bombard validate_project_name with extreme, malformed max_length types."""
    with pytest.raises(TypeError, match="(?i)must be int"):
        validate_project_name("valid_name", max_length=max_length)


@given(
    allow_hyphen=st.one_of(
        st.none(),
        st.integers(),
        st.floats(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_project_name_malformed_allow_hyphen_expected(
    allow_hyphen,
) -> None:
    """Bombard validate_project_name with extreme, malformed allow_hyphen types."""
    with pytest.raises(TypeError, match="(?i)must be bool"):
        validate_project_name("valid_name", allow_hyphen=allow_hyphen)


@given(
    allow_underscore=st.one_of(
        st.none(),
        st.integers(),
        st.floats(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_project_name_malformed_allow_underscore_expected(
    allow_underscore,
) -> None:
    """Bombard validate_project_name with extreme, malformed allow_underscore types."""
    with pytest.raises(TypeError, match="(?i)must be bool"):
        validate_project_name("valid_name", allow_underscore=allow_underscore)
