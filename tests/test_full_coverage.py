"""Additional tests for 100% coverage - Part 2."""

from __future__ import annotations

from pathlib import Path

import pytest


class TestLoggingFullCoverage:
    """Additional tests for logging module full coverage."""

    def test_stack_logger_debug(self) -> None:
        """Test StackLogger debug method."""
        from stack.utils.logging import StackLogger

        logger = StackLogger(level="DEBUG")
        logger.debug("Debug message", extra_key="value")

    def test_stack_logger_warning(self) -> None:
        """Test StackLogger warning method."""
        from stack.utils.logging import StackLogger

        logger = StackLogger()
        logger.warning("Warning message", warning_type="test")

    def test_stack_logger_error(self) -> None:
        """Test StackLogger error method."""
        from stack.utils.logging import StackLogger

        logger = StackLogger()
        logger.error("Error message", error_code=500)

    def test_stack_logger_critical(self) -> None:
        """Test StackLogger critical method."""
        from stack.utils.logging import StackLogger

        logger = StackLogger()
        logger.critical("Critical message", severity="high")

    def test_stack_logger_exception(self) -> None:
        """Test StackLogger exception method."""
        from stack.utils.logging import StackLogger

        logger = StackLogger()
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("Caught exception", caught=True)

    def test_setup_logging_json_format(self) -> None:
        """Test setup_logging with JSON format."""
        from stack.utils.logging import setup_logging

        setup_logging(level="INFO", format_type="json")

    def test_setup_logging_simple_format(self) -> None:
        """Test setup_logging with simple format."""
        from stack.utils.logging import setup_logging

        setup_logging(level="WARNING", format_type="simple")

    def test_setup_logging_with_file(self, tmp_path: Path) -> None:
        """Test setup_logging with file handler."""
        from stack.utils.logging import setup_logging

        log_file = tmp_path / "test.log"
        setup_logging(level="INFO", log_file=str(log_file))

    def test_get_logger(self) -> None:
        """Test get_logger function."""
        from stack.utils.logging import get_logger

        logger = get_logger("my_app", level="DEBUG")
        logger.info("Using get_logger")


class TestSubprocessFullCoverage:
    """Additional tests for subprocess module full coverage."""

    def test_run_safe_command_timeout(self) -> None:
        """Test run_safe_command with timeout."""
        from stack.utils.subprocess import run_safe_command

        result = run_safe_command(["echo", "quick"], timeout=30)
        assert result.success

    def test_run_safe_command_cwd(self, tmp_path: Path) -> None:
        """Test run_safe_command with working directory."""
        from stack.utils.subprocess import run_safe_command

        result = run_safe_command(["ls"], cwd=tmp_path)
        assert result.success


class TestGeneratorsFullCoverage:
    """Additional tests for generators module full coverage."""

    def test_generate_pre_commit_with_all_hooks(self) -> None:
        """Test generate_pre_commit_config with all security hooks."""
        from stack.config.generators import generate_pre_commit_config
        from stack.config.models import SecurityConfig, StackConfig

        security = SecurityConfig(
            level="paranoid",
            enable_bandit=True,
            enable_safety=True,
            enable_semgrep=True,
            enable_detect_secrets=True,
        )
        config = StackConfig(project_name="test-project", security=security)
        result = generate_pre_commit_config(config)

        assert "bandit" in result
        assert "safety" in result
        assert "semgrep" in result
        assert "detect-secrets" in result
        assert "pip-audit" in result  # paranoid level


class TestGuardsFullCoverage:
    """Additional tests for guards module full coverage."""

    def test_guard_env_sensitive_pattern_allowed(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test guard_env_variable with allowed sensitive pattern."""
        from stack.security.guards import guard_env_variable

        monkeypatch.setenv("MY_SECRET_KEY", "allowed_value")
        result = guard_env_variable(
            "MY_SECRET_KEY",
            allowed_names=["MY_SECRET_KEY"],
        )
        assert result == "allowed_value"


class TestValidatorsFullCoverage:
    """Additional tests for validators module full coverage."""

    def test_validate_email_invalid_format(self) -> None:
        """Test validate_email with invalid format."""
        from stack.security.validators import validate_email

        with pytest.raises(ValueError):
            validate_email("not-an-email")

    def test_validate_url_missing_scheme(self) -> None:
        """Test validate_url with missing scheme."""
        from stack.security.validators import validate_url

        with pytest.raises(ValueError):
            validate_url("example.com")


class TestSanitizersFullCoverage:
    """Additional tests for sanitizers module full coverage."""

    def test_sanitize_string_removes_html(self) -> None:
        """Test sanitize_string removes HTML tags."""
        from stack.security.sanitizers import sanitize_string

        result = sanitize_string("<div>Safe</div><script>evil()</script>")
        assert "<script>" not in result
        assert "<div>" not in result

    def test_sanitize_sql_identifier_valid(self) -> None:
        """Test sanitize_sql_identifier valid cases."""
        from stack.security.sanitizers import sanitize_sql_identifier

        result = sanitize_sql_identifier("valid_column_name")
        assert result == "valid_column_name"

    def test_sanitize_sql_identifier_removes_special(self) -> None:
        """Test sanitize_sql_identifier removes special chars."""
        from stack.security.sanitizers import sanitize_sql_identifier

        result = sanitize_sql_identifier("col'; DROP TABLE--")
        assert "'" not in result
        assert ";" not in result


class TestCircuitBreakerFullCoverage:
    """Additional tests for circuit breaker full coverage."""

    def test_circuit_breaker_failure_count(self) -> None:
        """Test circuit breaker failure count property."""
        from stack.utils.circuit_breaker import CircuitBreaker

        breaker = CircuitBreaker(failure_threshold=5)

        @breaker
        def failing() -> None:
            raise ValueError("fail")

        for _ in range(3):
            with pytest.raises(ValueError):
                failing()

        assert breaker.failure_count == 3


class TestFilesystemFullCoverage:
    """Additional tests for filesystem full coverage."""

    def test_ensure_dir_with_mode(self, tmp_path: Path) -> None:
        """Test ensure_dir with custom mode."""
        from stack.utils.filesystem import ensure_dir

        new_dir = tmp_path / "new_dir"
        result = ensure_dir(new_dir, mode=0o700)
        assert result.exists()

    def test_safe_delete_missing_ok(self, tmp_path: Path) -> None:
        """Test safe_delete with missing_ok=True."""
        from stack.utils.filesystem import safe_delete

        nonexistent = tmp_path / "nonexistent.txt"
        safe_delete(nonexistent, missing_ok=True)  # Should not raise

    def test_safe_delete_file(self, tmp_path: Path) -> None:
        """Test safe_delete deletes a file."""
        from stack.utils.filesystem import safe_delete

        test_file = tmp_path / "to_delete.txt"
        test_file.write_text("content")

        safe_delete(test_file)
        assert not test_file.exists()


class TestRetryFullCoverage:
    """Additional tests for retry full coverage."""

    def test_retry_decorator_log_retries(self) -> None:
        """Test retry decorator with log_retries=False."""
        from stack.utils.retry import retry

        call_count = 0

        @retry(max_attempts=2, initial_delay=0.01, log_retries=False, on=(ValueError,))
        def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("fail")
            return "ok"

        result = flaky()
        assert result == "ok"
        assert call_count == 2
