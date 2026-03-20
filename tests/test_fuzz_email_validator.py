import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.validators import validate_email


@given(st.text())
def test_fuzz_validate_email(email_input):
    try:
        validated = validate_email(email_input)
        # If it is considered a valid email, it MUST NOT contain newlines or null bytes
        # to prevent CRLF injection and other bypasses.
        assert "\n" not in validated
        assert "\r" not in validated
        assert "\0" not in validated
    except (ValueError, TypeError):
        pass


def test_validate_email_newline_bypass():
    # Explicitly test the bypass
    email = "admin@example.com\n"
    with pytest.raises(ValueError):
        validate_email(email)
