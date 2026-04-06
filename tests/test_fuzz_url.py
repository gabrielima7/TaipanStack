import contextlib

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_url


def test_url_dos_length() -> None:
    """Fuzz to verify protection against insanely large URLs triggering port/int issues."""
    huge_url = "http://localhost:" + "1" * 500000
    with pytest.raises(ValueError, match="exceeds maximum length"):
        validate_url(huge_url)


def test_url_with_credentials() -> None:
    """Test standard valid URL format with credentials."""
    url = "http://user:pass@example.com/path"
    assert validate_url(url) == url


def test_url_ipv6() -> None:
    """Test IPv6 localhost logic and parsing."""
    url = "http://[::1]:8080/"
    assert validate_url(url) == url


def test_url_ipv6_with_credentials() -> None:
    """Test IPv6 URL format with credentials."""
    url = "http://user:pass@[::1]:8080/"
    assert validate_url(url) == url


@given(st.text())
@settings(max_examples=500)
def test_validate_url_hypothesis(text: str) -> None:
    """General property-based fuzzer ensuring random garbage doesn't crash."""
    with contextlib.suppress(ValueError, TypeError):
        validate_url(text)
