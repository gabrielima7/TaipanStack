"""Property-based fuzzing tests for sanitize_filename replacement parameter."""

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import sanitize_filename


@given(
    replacement=st.one_of(
        st.integers(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_sanitize_filename_malformed_replacement_expected(
    replacement,
) -> None:
    """Bombard sanitize_filename with extreme, malformed replacement types."""
    import pytest

    with pytest.raises(TypeError, match="(?i)must be str"):
        sanitize_filename("bad\\file<>", replacement=replacement)


@given(
    preserve_extension=st.one_of(
        st.integers(),
        st.floats(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_sanitize_filename_malformed_preserve_extension_expected(
    preserve_extension,
) -> None:
    """Bombard sanitize_filename with extreme, malformed preserve_extension types."""
    import pytest

    with pytest.raises(TypeError, match="(?i)must be bool"):
        sanitize_filename("bad\\file<>", preserve_extension=preserve_extension)


@given(
    max_length=st.one_of(
        st.text(),
        st.floats(),
        st.booleans(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_sanitize_filename_malformed_max_length_expected(
    max_length,
) -> None:
    """Bombard sanitize_filename with extreme, malformed max_length types."""
    import pytest

    with pytest.raises(TypeError, match="(?i)must be int"):
        sanitize_filename("bad\\file<>", max_length=max_length)
