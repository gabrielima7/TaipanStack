"""Additional tests for filesystem, logging, and other modules for 100% coverage."""

from pathlib import Path
from unittest.mock import patch

import pytest

from taipanstack.core.result import Err
from taipanstack.security.guards import SecurityError


class TestFilesystemEdgeCases:
    """Edge case tests for filesystem module."""

    def test_edge_cases_coverage_safe_read_with_traversal_no_base_dir_expected(
        self, tmp_path: Path
    ) -> None:
        """Test safe_read with .. in path but no base_dir uses cwd."""
        from taipanstack.utils.filesystem import safe_read

        # Create a file in tmp_path
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # This should fail because .. triggers guard with cwd
        result = safe_read(tmp_path / ".." / "etc" / "passwd")
        match result:
            case Err(SecurityError()):
                pass
            case _:
                pytest.fail("Expected Err(SecurityError)")

    def test_edge_cases_coverage_safe_write_existing_file_guarded_expected(
        self, tmp_path: Path
    ) -> None:
        """Test safe_write with existing file and base_dir."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "existing.txt"
        test_file.write_text("old content")

        result = safe_write(
            test_file, "new content", options=WriteOptions(base_dir=tmp_path)
        )
        assert result.read_text() == "new content"

    def test_edge_cases_coverage_safe_write_with_traversal_no_base_dir_expected(
        self, tmp_path: Path
    ) -> None:
        """Test safe_write with .. triggers guard."""
        from taipanstack.utils.filesystem import safe_write

        with pytest.raises(SecurityError):
            safe_write(tmp_path / ".." / "bad.txt", "content")

    def test_edge_cases_coverage_safe_write_atomic_error_cleanup_expected(
        self, tmp_path: Path
    ) -> None:
        """Test atomic write cleans up temp file on error."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        test_file = tmp_path / "test.txt"

        # Mock write_text to raise an error
        with patch.object(Path, "write_text", side_effect=OSError("Write error")):
            with pytest.raises(OSError):
                safe_write(test_file, "content", options=WriteOptions(atomic=True))


class TestLoggingEdgeCases:
    """Edge case tests for logging module."""

    def test_edge_cases_coverage_stack_logger_bind_context_expected(self) -> None:
        """Test StackLogger with bind context."""
        from taipanstack.utils.logging import StackLogger

        logger = StackLogger()
        logger.bind(user="test", request_id="123")

        # Log something - context should be in logs
        logger.info("Test message")

    def test_edge_cases_coverage_stack_logger_unbind_context_expected(self) -> None:
        """Test unbinding logger context."""
        from taipanstack.utils.logging import StackLogger

        logger = StackLogger()
        logger.bind(key="value")
        logger.unbind("key")

        logger.info("After unbind")

    def test_edge_cases_coverage_setup_logging_basic_expected(self) -> None:
        """Test setup_logging basic configuration."""
        from taipanstack.utils.logging import setup_logging

        setup_logging(level="DEBUG")

    def test_edge_cases_coverage_log_operation_decorator_expected(self) -> None:
        """Test log_operation decorator."""
        from taipanstack.utils.logging import log_operation

        @log_operation("test_op")
        def my_func(x: int) -> int:
            return x * 2

        result = my_func(5)
        assert result == 10

    def test_log_operation_with_error(self) -> None:
        """Test log_operation decorator with error."""
        from taipanstack.utils.logging import log_operation

        @log_operation("failing_op")
        def failing_func() -> None:
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_func()


class TestDecoratorsEdgeCases:
    """Edge case tests for decorators module."""

    def test_edge_cases_coverage_timeout_with_signal_expected(self) -> None:
        """Test timeout with signal (Unix only)."""
        import platform

        if platform.system() == "Windows":
            pytest.skip("Signal timeout not available on Windows")

        from taipanstack.security.decorators import OperationTimeoutError, timeout

        @timeout(0.1, use_signal=True)
        def slow_func() -> None:
            import time

            time.sleep(1)

        with pytest.raises(OperationTimeoutError):
            slow_func()


class TestGuardsEdgeCases:
    """Edge case tests for guards module."""

    def test_edge_cases_coverage_guard_command_injection_with_whitelist_expected(
        self,
    ) -> None:
        """Test guard_command_injection with custom whitelist."""
        from taipanstack.security.guards import guard_command_injection

        cmd = ["python", "--version"]
        result = guard_command_injection(cmd, allowed_commands=["python", "pip"])
        assert result == cmd


class TestSanitizersEdgeCases:
    """Edge case tests for sanitizers module."""

    def test_edge_cases_coverage_sanitize_string_with_null_bytes_expected(self) -> None:
        """Test sanitizing string with null bytes."""
        from taipanstack.security.sanitizers import sanitize_string

        result = sanitize_string("hello\x00world")
        assert "\x00" not in result

    def test_edge_cases_coverage_sanitize_path_with_special_chars_expected(
        self,
    ) -> None:
        """Test sanitizing path with special characters."""
        from taipanstack.security.sanitizers import sanitize_path

        result = sanitize_path("/path/to/../file")
        assert ".." not in str(result)


class TestValidatorsEdgeCases:
    """Edge case tests for validators module."""

    def test_edge_cases_coverage_validate_project_name_reserved_expected(self) -> None:
        """Test that reserved names are rejected."""
        from taipanstack.security.validators import validate_project_name

        with pytest.raises(ValueError, match="reserved"):
            validate_project_name("test")

    def test_edge_cases_coverage_validate_url_with_ip_expected(self) -> None:
        """Test validating URL with IP address."""
        from taipanstack.security.validators import validate_url

        result = validate_url("http://192.168.1.1:8080", require_tld=False)
        assert "192.168.1.1" in result


class TestRetryEdgeCases:
    """Edge case tests for retry module."""

    def test_edge_cases_coverage_retrier_multiple_attempts_expected(self) -> None:
        """Test Retrier with a loop for multiple attempts."""
        from taipanstack.resilience.retry import Retrier

        retrier = Retrier(max_attempts=3, initial_delay=0.01, on=(ValueError,))
        attempt_count = 0

        while True:
            try:
                with retrier:
                    attempt_count += 1
                    if attempt_count < 3:
                        raise ValueError("fail")
                    break  # Success
            except ValueError:
                if retrier.attempt >= retrier.config.max_attempts:
                    raise

        assert attempt_count == 3


class TestSubprocessEdgeCases:
    """Edge case tests for subprocess module."""

    def test_edge_cases_coverage_run_safe_command_with_env_expected(self) -> None:
        """Test run_safe_command with custom environment."""
        from taipanstack.utils.subprocess import run_safe_command

        result = run_safe_command(
            ["echo", "test"],
            env={"CUSTOM_VAR": "value"},
        )
        assert result.success


class TestCircuitBreakerEdgeCases:
    """Edge case tests for circuit breaker module."""

    def test_edge_cases_coverage_circuit_breaker_half_open_success_expected(
        self,
    ) -> None:
        """Test circuit transitions from half-open to closed."""
        import time

        from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

        breaker = CircuitBreaker(
            failure_threshold=1,
            success_threshold=2,
            timeout=0.05,
        )
        attempt = 0

        @breaker
        def func() -> str:
            nonlocal attempt
            attempt += 1
            if attempt == 1:
                raise ValueError("first fail")
            return "ok"

        # Trip circuit
        with pytest.raises(ValueError):
            func()

        assert breaker.state == CircuitState.OPEN

        # Wait for half-open
        time.sleep(0.1)

        # First success in half-open
        func()

        # Second success should close
        func()

        assert breaker.state == CircuitState.CLOSED
