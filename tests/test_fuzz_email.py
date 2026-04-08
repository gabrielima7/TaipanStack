import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import (
    MAX_EMAIL_DOMAIN_LENGTH,
    MAX_EMAIL_LOCAL_LENGTH,
    validate_email,
)


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=200,
)
@given(
    st.text(
        min_size=MAX_EMAIL_LOCAL_LENGTH + MAX_EMAIL_DOMAIN_LENGTH + 10,
        max_size=MAX_EMAIL_LOCAL_LENGTH + MAX_EMAIL_DOMAIN_LENGTH + 1000,
    )
)
def test_fuzz_email_massive_strings_dos(email: str) -> None:
    """Fuzz validate_email with massive strings to ensure DoS protection limits are active."""
    with pytest.raises(
        ValueError,
        match="Email length exceeds maximum allowed|Invalid email format|Email local part exceeds|Email domain exceeds",
    ):
        validate_email(email)


@given(
    st.text(
        alphabet=st.characters(
            exclude_categories=("Cc",),
        ),
        min_size=9,
        max_size=99,
    ).map(lambda s: s + "\x00")
)
@settings(max_examples=200, suppress_health_check=[HealthCheck.filter_too_much])
def test_fuzz_email_null_bytes(email: str) -> None:
    """Fuzz validate_email with strings containing null bytes."""
    with pytest.raises(
        ValueError, match="Email contains invalid characters|Invalid email format"
    ):
        validate_email(email)


@given(
    st.text(
        alphabet=st.characters(
            exclude_characters=["\x00"], min_codepoint=0x200B, max_codepoint=0x200F
        ),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=200, suppress_health_check=[HealthCheck.filter_too_much])
def test_fuzz_email_unprintable_chars(chars: str) -> None:
    """Fuzz validate_email with zero-width characters and unprintable unicode."""
    email = f"test{chars}@example.com"
    with pytest.raises(
        ValueError, match="Email contains invalid characters|Invalid email format"
    ):
        validate_email(email)


def test_email_null_byte_dos() -> None:
    """Explicitly test null bytes in email format."""
    with pytest.raises(
        ValueError, match="Email contains invalid characters|Invalid email format"
    ):
        validate_email("test\x00@example.com")
