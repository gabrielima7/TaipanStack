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

    def test_name_too_long(self) -> None:
        """Test that names exceeding max_length are rejected."""
        long_name = "a" * 101
        with pytest.raises(ValueError, match="exceeds maximum"):
            validate_project_name(long_name, max_length=100)

    def test_name_starts_with_number(self) -> None:
        """Test that names starting with numbers are rejected."""
        with pytest.raises(ValueError, match="start with a letter"):
            validate_project_name("123project")

    def test_name_starts_with_hyphen(self) -> None:
        """Test that names starting with hyphen are rejected."""
        with pytest.raises(ValueError, match="start with a letter"):
            validate_project_name("-myproject")

    def test_hyphen_not_allowed(self) -> None:
        """Test that hyphens can be disallowed."""
        with pytest.raises(ValueError, match="invalid characters"):
            validate_project_name("my-project", allow_hyphen=False)

    def test_underscore_not_allowed(self) -> None:
        """Test that underscores can be disallowed."""
        with pytest.raises(ValueError, match="invalid characters"):
            validate_project_name("my_project", allow_underscore=False)

    def test_empty_name(self) -> None:
        """Test that empty names are rejected."""
        with pytest.raises(ValueError):
            validate_project_name("")


class TestValidatePythonVersionEdgeCases:
    """Additional tests for validate_python_version."""

    def test_unsupported_major_version(self) -> None:
        """Test that unsupported major versions are rejected."""
        with pytest.raises(ValueError, match="Python 3"):
            validate_python_version("2.7")

    def test_unsupported_minor_version(self) -> None:
        """Test that old minor versions are rejected."""
        with pytest.raises(ValueError, match="3.10"):
            validate_python_version("3.9")

    def test_version_number_conversion_error(self) -> None:
        """Test that extremely long version numbers are rejected."""
        # This triggers the except ValueError block due to integer string conversion limit
        with pytest.raises(ValueError, match="Invalid version numbers"):
            validate_python_version("1." + "9" * 5000)

    def test_non_numeric_version_mock(self) -> None:
        """Test that a non-numeric version string correctly raises ValueError during integer conversion when bypassing regex."""
        from unittest.mock import patch

        with patch("taipanstack.security.validators.re.match") as mock_match:
            mock_match.return_value = True
            with pytest.raises(ValueError, match="Invalid version numbers in 'a.b'"):
                validate_python_version("a.b")


class TestValidateEmailEdgeCases:
    """Additional tests for validate_email."""

    def test_local_part_too_long(self) -> None:
        """Test that local part exceeding max length is rejected."""
        long_local = "a" * 65
        with pytest.raises(ValueError):
            validate_email(f"{long_local}@example.com")

    def test_domain_too_long(self) -> None:
        """Test that domain exceeding max length is rejected."""
        long_domain = "a" * 256
        with pytest.raises(ValueError):
            validate_email(f"test@{long_domain}.com")


class TestValidateUrlEdgeCases:
    """Additional tests for validate_url."""

    def test_invalid_scheme(self) -> None:
        """Test that invalid schemes are rejected."""
        with pytest.raises(ValueError, match="scheme"):
            validate_url("ftp://example.com")

    def test_missing_domain(self) -> None:
        """Test that URLs without domain are rejected."""
        with pytest.raises(ValueError):
            validate_url("http://")

    def test_localhost_allowed(self) -> None:
        """Test that localhost is allowed when TLD not required."""
        result = validate_url("http://localhost:8080", require_tld=False)
        assert "localhost" in result

