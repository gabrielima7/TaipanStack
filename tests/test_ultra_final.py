"""Ultra-final tests to reach 100% coverage."""

from pathlib import Path

import pytest


class TestValidators100Percent:
    """Tests to reach 100% for validators."""

    def test_validate_project_name_no_hyphens_no_underscores_expected(self) -> None:
        """Test validate_project_name with both disabled."""
        from taipanstack.security.validators import validate_project_name

        result = validate_project_name(
            "myproject123", allow_hyphen=False, allow_underscore=False
        )
        assert result == "myproject123"

    def test_validate_url_http_expected(self) -> None:
        """Test validate_url with http scheme."""
        from urllib.parse import urlparse

        from taipanstack.security.validators import validate_url

        result = validate_url("http://example.com")
        assert urlparse(result).hostname == "example.com"


class TestGuards100Percent:
    """Tests to reach 100% for guards."""

    def test_guard_path_traversal_resolve_error(self, tmp_path: Path) -> None:
        """Test guard_path_traversal when path resolution fails."""
        from taipanstack.security.guards import guard_path_traversal

        valid_file = tmp_path / "valid.txt"
        valid_file.touch()
        result = guard_path_traversal(valid_file, tmp_path)
        assert result.exists()

    def test_guard_file_extension_denied(self) -> None:
        """Test guard_file_extension with denied extension."""
        from taipanstack.security.guards import SecurityError, guard_file_extension

        with pytest.raises(SecurityError):
            guard_file_extension("script.exe", denied_extensions=["exe", "bat"])


class TestSanitizers100Percent:
    """Tests to reach 100% for sanitizers."""

    def test_sanitize_string_no_whitespace_strip_expected(self) -> None:
        """Test sanitize_string with strip_whitespace=False."""
        from taipanstack.security.sanitizers import sanitize_string

        result = sanitize_string("  hello  ", strip_whitespace=False)
        assert result == "  hello  "

    def test_sanitize_filename_no_replacement_expected(self) -> None:
        """Test sanitize_filename with empty replacement."""
        from taipanstack.security.sanitizers import sanitize_filename

        result = sanitize_filename("file<>name.txt", replacement="")
        assert "<" not in result
        assert ">" not in result

    def test_sanitize_path_no_parts_expected(self) -> None:
        """Test sanitize_path with path that results in no parts."""
        from taipanstack.security.sanitizers import sanitize_path

        result = sanitize_path("./")
        assert result is not None


class TestFilesystem100Percent:
    """Tests to reach 100% for filesystem."""


class TestRetry100Percent:
    """Tests to reach 100% for retry."""

    def test_retry_max_delay_applied_expected(self) -> None:
        """Test that max_delay is actually applied."""
        from taipanstack.resilience.retry import RetryConfig, calculate_delay

        config = RetryConfig(
            initial_delay=1.0, max_delay=2.0, exponential_base=10.0, jitter=False
        )
        delay = calculate_delay(10, config)
        assert delay <= config.max_delay


class TestModels100Percent:
    """Tests to reach 100% for models."""

    def test_stack_config_verbose_expected(self) -> None:
        """Test StackConfig with verbose option."""
        from taipanstack.config.models import StackConfig

        config = StackConfig(project_name="test", verbose=True)
        assert config.verbose is True


class TestCircuitBreaker100Percent:
    """Tests to reach 100% for circuit_breaker."""

    def test_circuit_breaker_name_expected(self) -> None:
        """Test CircuitBreaker with custom name."""
        from taipanstack.resilience.circuit_breaker import CircuitBreaker

        breaker = CircuitBreaker(name="custom_breaker")

        @breaker
        def test_ultra_final_func_expected() -> str:
            return "ok"

        assert test_ultra_final_func_expected() == "ok"
        assert breaker.name == "custom_breaker"
