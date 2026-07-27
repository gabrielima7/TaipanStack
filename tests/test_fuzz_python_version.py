import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import (
    MAX_PYTHON_VERSION_LENGTH,
    validate_python_version,
)


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=200,
)
@given(
    st.text(
        min_size=MAX_PYTHON_VERSION_LENGTH + 1,
        max_size=MAX_PYTHON_VERSION_LENGTH + 1000,
    )
)
def test_fuzz_python_version_fuzz_version_massive_strings_dos(
    version: str,
) -> None:
    """Fuzz validate_python_version with massive strings to ensure DoS protection limits are active."""
    with pytest.raises(ValueError, match="Version string exceeds maximum length"):
        validate_python_version(version)


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cc",), whitelist_characters=["\x00"]
        ),
        min_size=1,
        max_size=15,
    ).filter(lambda s: "\x00" in s)
)
def test_fuzz_python_version_fuzz_version_null_bytes_expected(
    version: str,
) -> None:
    """Fuzz validate_python_version with strings containing null bytes."""
    with pytest.raises(ValueError, match="Version contains invalid characters"):
        validate_python_version(version)


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_characters=["\x00"], min_codepoint=0x200B, max_codepoint=0x200F
        ),
        min_size=1,
        max_size=10,
    )
)
def test_fuzz_python_version_fuzz_version_unprintable_chars_expected(
    chars: str,
) -> None:
    """Fuzz validate_python_version with zero-width characters and unprintable unicode."""
    version = f"3.{chars}"
    with pytest.raises(ValueError, match="Version contains invalid characters"):
        validate_python_version(version)


def test_fuzz_python_version_version_unicode_digits_expected() -> None:
    """Ensure validate_python_version does not accept unicode digits like arabic numerals."""
    version = "٣.١٢"
    with pytest.raises(ValueError, match="Invalid version format"):
        validate_python_version(version)
