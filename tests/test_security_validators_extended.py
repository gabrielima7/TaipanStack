"""Additional tests for validators to achieve 100% coverage."""

import pytest

from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
    validate_url,
)


class TestValidateProjectNameEdgeCases:
    """Additional tests for validate_project_name."""

    def test_security_validators_extended_name_too_long(self) -> None:
        """Test that names exceeding max_length are rejected."""
        long_name = "a" * 101
        with pytest.raises(ValueError, match="exceeds maximum"):
            validate_project_name(long_name, max_length=100)

    def test_security_validators_extended_name_starts_with_number(
        self,
    ) -> None:
        """Test that names starting with numbers are rejected."""
        with pytest.raises(ValueError, match="start with a letter"):
            validate_project_name("123project")

    def test_security_validators_extended_name_starts_with_hyphen(
        self,
    ) -> None:
        """Test that names starting with hyphen are rejected."""
        with pytest.raises(ValueError, match="start with a letter"):
            validate_project_name("-myproject")

    def test_security_validators_extended_hyphen_not_allowed(self) -> None:
        """Test that hyphens can be disallowed."""
        with pytest.raises(ValueError, match="invalid characters"):
            validate_project_name("my-project", allow_hyphen=False)

    def test_security_validators_extended_underscore_not_allowed(self) -> None:
        """Test that underscores can be disallowed."""
        with pytest.raises(ValueError, match="invalid characters"):
            validate_project_name("my_project", allow_underscore=False)

    def test_security_validators_extended_empty_name(self) -> None:
        """Test that empty names are rejected."""
        with pytest.raises(ValueError):
            validate_project_name("")


class TestValidatePythonVersionEdgeCases:
    """Additional tests for validate_python_version."""

    def test_security_validators_extended_unsupported_major_version(
        self,
    ) -> None:
        """Test that unsupported major versions are rejected."""
        with pytest.raises(ValueError, match="Python 3"):
            validate_python_version("2.7")

    def test_security_validators_extended_unsupported_minor_version(
        self,
    ) -> None:
        """Test that old minor versions are rejected."""
        with pytest.raises(ValueError, match="3.10"):
            validate_python_version("3.9")

    def test_security_validators_extended_version_number_conversion_error(
        self,
    ) -> None:
        """Test that extremely long version numbers are rejected."""
        # This now triggers the length boundary check preventing DoS
        with pytest.raises(ValueError, match="Version string exceeds maximum length"):
            validate_python_version("1." + "9" * 5000)

    def test_security_validators_extended_non_numeric_version_mock(
        self,
    ) -> None:
        """Test that a non-numeric version string correctly raises ValueError during integer conversion when bypassing regex."""
        from unittest.mock import patch

        with patch("taipanstack.security.validators.re.match") as mock_match:
            mock_match.return_value = True
            with pytest.raises(ValueError, match="Invalid version numbers in 'a.b'"):
                validate_python_version("a.b")


class TestValidateEmailEdgeCases:
    """Additional tests for validate_email."""

    def test_security_validators_extended_local_part_too_long(self) -> None:
        """Test that local part exceeding max length is rejected."""
        long_local = "a" * 65
        with pytest.raises(ValueError):
            validate_email(f"{long_local}@example.com")

    def test_security_validators_extended_domain_too_long(self) -> None:
        """Test that domain exceeding max length is rejected."""
        long_domain = "a" * 256
        with pytest.raises(ValueError):
            validate_email(f"test@{long_domain}.com")


class TestValidateUrlEdgeCases:
    """Additional tests for validate_url."""

    def test_security_validators_extended_invalid_scheme(self) -> None:
        """Test that invalid schemes are rejected."""
        with pytest.raises(ValueError, match="scheme"):
            validate_url("ftp://example.com")

    def test_security_validators_extended_missing_domain(self) -> None:
        """Test that URLs without domain are rejected."""
        with pytest.raises(ValueError):
            validate_url("http://")

    def test_security_validators_extended_localhost_allowed(self) -> None:
        """Test that localhost is allowed when TLD not required."""
        result = validate_url("http://localhost:8080", require_tld=False)
        assert "localhost" in result


# Migrated from tests/test_fuzz_email_operations.py
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=200,
)
@given(st.text(min_size=321, max_size=5000))
def test_fuzz_email_massive_strings_dos(email: str) -> None:
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
def test_fuzz_email_null_bytes(email: str) -> None:
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
def test_fuzz_email_unprintable_chars(chars: str) -> None:
    """Fuzz validate_email with zero-width characters and unprintable unicode."""
    email = f"user@{chars}.com"
    with pytest.raises(ValueError, match="Email contains invalid characters"):
        validate_email(email)


# Migrated from tests/test_fuzz_index_error.py
import contextlib

from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.validators import _check_project_name_chars


@given(st.text())
def test_fuzz_project_name_chars(text):
    if text == "":
        try:
            _check_project_name_chars(text, True, True)
        except ValueError:
            pass
        except IndexError:
            pytest.fail("IndexError was raised instead of ValueError")
    else:
        with contextlib.suppress(ValueError):
            _check_project_name_chars(text, True, True)


# Migrated from tests/test_fuzz_python_version_operations.py
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import MAX_PYTHON_VERSION_LENGTH


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
def test_fuzz_python_version_fuzz_version_null_bytes(version: str) -> None:
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
def test_fuzz_python_version_fuzz_version_unprintable_chars(
    chars: str,
) -> None:
    """Fuzz validate_python_version with zero-width characters and unprintable unicode."""
    version = f"3.{chars}"
    with pytest.raises(ValueError, match="Version contains invalid characters"):
        validate_python_version(version)


def test_fuzz_python_version_version_unicode_digits() -> None:
    """Ensure validate_python_version does not accept unicode digits like arabic numerals."""
    version = "٣.١٢"
    with pytest.raises(ValueError, match="Invalid version format"):
        validate_python_version(version)


# Migrated from tests/test_fuzz_url_security_operations.py
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import MAX_URL_LENGTH


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=200,
)
@given(st.text(min_size=MAX_URL_LENGTH + 1, max_size=MAX_URL_LENGTH + 1000))
def test_fuzz_url_security_fuzz_url_massive_strings_dos(url: str) -> None:
    """Fuzz validate_url with massive strings to ensure DoS protection limits are active."""
    with pytest.raises(ValueError, match="URL length exceeds maximum allowed"):
        validate_url(url)


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
def test_fuzz_url_security_fuzz_url_null_bytes(url: str) -> None:
    """Fuzz validate_url with strings containing null bytes."""
    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url)


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
def test_fuzz_url_security_fuzz_url_unprintable_chars(chars: str) -> None:
    """Fuzz validate_url with zero-width characters and unprintable unicode."""
    url = f"http://example.com/{chars}"
    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url)


def test_fuzz_url_security_url_port_integer_conversion_dos() -> None:
    """Explicitly test huge port sizes that crash URL parsers."""
    url = "http://example.com:" + "9" * 10000
    with pytest.raises(ValueError, match="URL length exceeds maximum allowed"):
        validate_url(url)


def test_fuzz_url_security_url_tld_ipv6_handling() -> None:
    """Ensure validate_url uses parsed.hostname for localhost checks on IPv6."""
    url = "http://[::1]"
    # Should not raise
    assert validate_url(url) == url


def test_fuzz_url_security_url_credentials_bypassing_tld_check() -> None:
    """Ensure credentials don't mess up the TLD checks because of manual splits on netloc."""
    url = "http://user:pass@notlocalhost"
    # missing TLD, and not localhost, so should raise
    with pytest.raises(ValueError, match="URL domain must have a TLD"):
        validate_url(url)
