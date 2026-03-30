"""Tests for stack.security.validators module."""

from unittest.mock import patch
from urllib.parse import urlparse

import pytest

from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
    validate_url,
)


class TestValidateProjectName:
    """Tests for validate_project_name function."""

    def test_valid_project_name(self) -> None:
        """Test valid project names pass."""
        assert validate_project_name("my_project") == "my_project"
        assert validate_project_name("MyProject") == "MyProject"
        assert validate_project_name("my-project") == "my-project"
        assert validate_project_name("myproject123") == "myproject123"

    def test_empty_name_rejected(self) -> None:
        """Test empty names are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_project_name("")

    def test_name_must_start_with_letter(self) -> None:
        """Test names must start with a letter."""
        with pytest.raises(ValueError, match="must start with a letter"):
            validate_project_name("123project")

    def test_reserved_names_rejected(self) -> None:
        """Test reserved names are rejected."""
        with pytest.raises(ValueError, match="is reserved"):
            validate_project_name("test")

    def test_max_length_enforced(self) -> None:
        """Test max length is enforced."""
        with pytest.raises(ValueError, match="exceeds maximum length"):
            validate_project_name("a" * 101)


class TestValidatePythonVersion:
    """Tests for validate_python_version function."""

    def test_valid_versions(self) -> None:
        """Test valid Python versions pass."""
        assert validate_python_version("3.10") == "3.10"
        assert validate_python_version("3.11") == "3.11"
        assert validate_python_version("3.12") == "3.12"

    def test_invalid_format_rejected(self) -> None:
        """Test invalid formats are rejected."""
        with pytest.raises(ValueError, match="Invalid version format"):
            validate_python_version("python3.10")

        with pytest.raises(ValueError, match="Invalid version format"):
            validate_python_version("3.10.5")

    def test_unsupported_version_rejected(self) -> None:
        """Test unsupported versions are rejected."""
        with pytest.raises(ValueError, match="not supported"):
            validate_python_version("3.9")

        with pytest.raises(ValueError, match="Only Python 3.x"):
            validate_python_version("2.7")

    def test_invalid_version_numbers_value_error(self) -> None:
        """Test ValueError is raised when version numbers are invalid."""
        from unittest.mock import patch

        with patch("taipanstack.security.validators.re.match") as mock_match:
            mock_match.return_value = True
            with pytest.raises(ValueError, match="Invalid version numbers in 'a.b'"):
                validate_python_version("a.b")


class TestValidateEmail:
    """Tests for validate_email function."""

    def test_valid_emails(self) -> None:
        """Test valid emails pass."""
        assert validate_email("user@example.com") == "user@example.com"
        assert validate_email("user.name@example.com") == "user.name@example.com"
        assert validate_email("user+tag@example.com") == "user+tag@example.com"

    def test_empty_email_rejected(self) -> None:
        """Test empty emails are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_email("")

    def test_invalid_format_rejected(self) -> None:
        """Test invalid formats are rejected."""
        with pytest.raises(ValueError, match="Invalid email format"):
            validate_email("not-an-email")

        with pytest.raises(ValueError, match="Invalid email format"):
            validate_email("user@")


class TestValidateUrl:
    """Tests for validate_url function."""

    def test_valid_urls(self) -> None:
        """Test valid URLs pass."""
        assert validate_url("https://example.com") == "https://example.com"
        assert validate_url("http://localhost:8080") == "http://localhost:8080"
        assert (
            validate_url("https://api.github.com/repos")
            == "https://api.github.com/repos"
        )

    def test_empty_url_rejected(self) -> None:
        """Test empty URLs are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_url("")

    def test_missing_scheme_rejected(self) -> None:
        """Test URLs without scheme are rejected."""
        with pytest.raises(ValueError, match="must have a scheme"):
            validate_url("example.com")

    def test_invalid_scheme_rejected(self) -> None:
        """Test invalid schemes are rejected."""
        with pytest.raises(ValueError, match="not allowed"):
            validate_url("ftp://example.com")

    def test_invalid_format_parsing_error(self) -> None:
        """Test URL parsing ValueError is caught and re-raised."""
        with pytest.raises(ValueError, match="Invalid URL format: Invalid IPv6 URL"):
            validate_url("http://[::1")

    def test_out_of_range_port_parsing_error(self) -> None:
        """Test URL with an out of range port raises ValueError."""
        with pytest.raises(ValueError, match="Invalid URL format: Port out of range"):
            validate_url("http://example.com:99999999999")


class TestValidatorsUncovered:
    """Tests for validators.py uncovered lines 128-130."""

    def test_python_version_parse_error(self) -> None:
        """Test validate_python_version with invalid numbers."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError, match="Invalid version format"):
            validate_python_version("abc")


class TestValidatorsMissingBranches:
    """Tests for validators missing branches."""

    def test_validate_project_name_with_hyphen_false(self) -> None:
        """Test validate_project_name with allow_hyphen=False."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError, match="invalid characters"):
            validate_project_name("my-project", allow_hyphen=False)

    def test_validate_project_name_with_underscore_false(self) -> None:
        """Test validate_project_name with allow_underscore=False."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError, match="invalid characters"):
            validate_project_name("my_project", allow_underscore=False)

    def test_validate_python_version_exact(self) -> None:
        """Test validate_python_version with exact version."""
        from taipanstack.security.validators import validate_python_version

        result = validate_python_version("3.11")
        assert result == "3.11"

    def test_validate_email_with_subdomain(self) -> None:
        """Test validate_email with subdomain."""
        from taipanstack.security.validators import validate_email

        result = validate_email("user@mail.example.com")
        assert result == "user@mail.example.com"


class TestValidatorsTLD:
    """Tests for validators URL TLD check (lines 235-236)."""

    def test_validate_url_no_tld(self) -> None:
        """Test validate_url with domain that has no TLD."""
        from taipanstack.security.validators import validate_url

        # Domain without TLD should fail
        with pytest.raises(ValueError, match="TLD"):
            validate_url("http://testserver/path")

    def test_validate_url_ends_with_dot(self) -> None:
        """Test validate_url with domain ending in dot."""
        from taipanstack.security.validators import validate_url

        with pytest.raises(ValueError, match="TLD"):
            validate_url("http://example./path")


class TestValidatorsParseError:
    """Tests for validators URL ValueError (lines 213-215)."""

    def test_validate_url_parse_error(self) -> None:
        """Test validate_url when urlparse raises ValueError."""
        from taipanstack.security.validators import validate_url

        # Force urlparse to raise ValueError by patching
        with patch("taipanstack.security.validators.urlparse") as mock_parse:
            mock_parse.side_effect = ValueError("Parse failed")
            with pytest.raises(ValueError, match="Invalid URL"):
                validate_url("http://valid.com")


class TestValidatorsEdgeCases:
    """Edge case tests for validators module."""

    def test_validate_project_name_reserved(self) -> None:
        """Test that reserved names are rejected."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError, match="reserved"):
            validate_project_name("test")

    def test_validate_url_with_ip(self) -> None:
        """Test validating URL with IP address."""
        from taipanstack.security.validators import validate_url

        result = validate_url("http://192.168.1.1:8080", require_tld=False)
        assert "192.168.1.1" in result


class TestValidatorsComplete:
    """Complete tests for validators module."""

    def test_validate_email_valid(self) -> None:
        """Test validate_email with valid email."""
        from taipanstack.security.validators import validate_email

        result = validate_email("user@example.com")
        assert result == "user@example.com"

    def test_validate_url_https(self) -> None:
        """Test validate_url with https."""
        from urllib.parse import urlparse

        from taipanstack.security.validators import validate_url

        result = validate_url("https://secure.example.com/path?query=1")
        parsed = urlparse(result)
        assert parsed.hostname == "secure.example.com"


class TestValidatorsFinalBranches:
    """Final tests for validators module to reach 100%."""

    def test_validate_project_name_starts_with_hyphen(self) -> None:
        """Test validate_project_name starting with hyphen."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError, match="start with"):
            validate_project_name("-myproject")

    def test_validate_email_invalid_domain(self) -> None:
        """Test validate_email with invalid domain."""
        from taipanstack.security.validators import validate_email

        with pytest.raises(ValueError):
            validate_email("user@")

    def test_validate_url_invalid_protocol(self) -> None:
        """Test validate_url with invalid protocol."""
        from taipanstack.security.validators import validate_url

        with pytest.raises(ValueError):
            validate_url("ftp://example.com", allowed_schemes=["http", "https"])


class TestValidatorsPythonVersionEdgeCases:
    """Test edge cases in Python version validation."""

    def test_validate_python_version_alpha_suffix(self) -> None:
        """Test version with non-numeric characters fails at regex."""
        with pytest.raises(ValueError, match="Invalid version format"):
            validate_python_version("3.12a")

    def test_validate_python_version_too_many_parts(self) -> None:
        """Test version with too many parts."""
        with pytest.raises(ValueError, match="Invalid version format"):
            validate_python_version("3.12.1")


class TestValidatorsBranches:
    """Tests for validator branches."""

    def test_validate_project_name_special_chars(self) -> None:
        """Test validate_project_name with special characters."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError):
            validate_project_name("project@name")

    def test_validate_python_version_invalid_format(self) -> None:
        """Test validate_python_version with invalid format."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError):
            validate_python_version("invalid")

    def test_validate_url_with_port(self) -> None:
        """Test validate_url with port number."""
        from taipanstack.security.validators import validate_url

        result = validate_url("https://example.com:443/path")
        parsed = urlparse(result)
        assert parsed.hostname == "example.com"


class TestValidatorsVersionInvalidBranch:
    """Test for validators.py lines 128-130: invalid version format."""

    def test_validate_python_version_invalid_numbers(self) -> None:
        """Test validate_python_version with non-numeric version parts."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError, match="Invalid version"):
            validate_python_version("3.abc")

    def test_validate_python_version_python2(self) -> None:
        """Test validate_python_version rejects Python 2."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError, match="Python 3"):
            validate_python_version("2.7")


class TestValidators100Percent:
    """Tests to reach 100% for validators."""

    def test_validate_project_name_no_hyphens_no_underscores(self) -> None:
        """Test validate_project_name with both disabled."""
        from taipanstack.security.validators import validate_project_name

        # Should work with just letters and numbers
        result = validate_project_name(
            "myproject123",
            allow_hyphen=False,
            allow_underscore=False,
        )
        assert result == "myproject123"

    def test_validate_url_http(self) -> None:
        """Test validate_url with http scheme."""
        from urllib.parse import urlparse

        from taipanstack.security.validators import validate_url

        result = validate_url("http://example.com")
        assert urlparse(result).hostname == "example.com"


class TestValidatorsVersionConversion:
    """Test for validators.py lines 128-130 (version conversion ValueError)."""

    def test_validate_python_version_with_letters(self) -> None:
        """Test validate_python_version with letters in version."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError, match="Invalid version"):
            validate_python_version("3.x")


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
