import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_email


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=200,
)
@given(st.text(min_size=321, max_size=5000))
def test_fuzz_email_massive_strings_dos_standard_expected(email: str) -> None:
    """Fuzz validate_email with massive strings to ensure DoS protection limits are active."""
    with pytest.raises(ValueError, match="Email length exceeds maximum allowed"):
        validate_email(email)


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cc",), whitelist_characters=["\x00"]
        ),
        min_size=10,
        max_size=100,
    ).filter(lambda s: "\x00" in s)
)
def test_fuzz_email_null_bytes_standard_expected(email: str) -> None:
    """Fuzz validate_email with strings containing null bytes."""
    with pytest.raises(ValueError, match="Email contains invalid characters"):
        validate_email(email)


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
def test_fuzz_email_unprintable_chars_standard_expected(chars: str) -> None:
    """Fuzz validate_email with zero-width characters and unprintable unicode."""
    email = f"user@{chars}.com"
    with pytest.raises(ValueError, match="Email contains invalid characters"):
        validate_email(email)
