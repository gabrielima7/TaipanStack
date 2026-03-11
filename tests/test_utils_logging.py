"""Tests for structured logging utilities."""

import logging
from pathlib import Path
from typing import Any

import pytest

from taipanstack.utils.context import set_correlation_id
from taipanstack.utils.logging import (
    DEFAULT_FORMAT,
    JSON_FORMAT,
    REDACTED_VALUE,
    StackLogger,
    correlation_id_processor,
    get_logger,
    log_operation,
    mask_sensitive_data_processor,
    setup_logging,
)


class TestStackLogger:
    """Tests for StackLogger class."""

    def test_init_with_defaults(self) -> None:
        """Test logger initialization with defaults."""
        logger = StackLogger()
        assert logger.name == "stack"
        assert logger.level == "INFO"

    def test_init_with_custom_name(self) -> None:
        """Test logger with custom name."""
        logger = StackLogger(name="my_module")
        assert logger.name == "my_module"

    def test_init_with_custom_level(self) -> None:
        """Test logger with custom level."""
        logger = StackLogger(level="DEBUG")
        assert logger.level == "DEBUG"

    def test_bind_adds_context(self) -> None:
        """Test that bind adds context."""
        logger = StackLogger()
        logger.bind(request_id="123", user="test")
        assert logger._context["request_id"] == "123"
        assert logger._context["user"] == "test"

    def test_bind_returns_self(self) -> None:
        """Test that bind returns self for chaining."""
        logger = StackLogger()
        result = logger.bind(key="value")
        assert result is logger

    def test_unbind_removes_context(self) -> None:
        """Test that unbind removes context keys."""
        logger = StackLogger()
        logger.bind(key1="value1", key2="value2")
        logger.unbind("key1")
        assert "key1" not in logger._context
        assert "key2" in logger._context

    def test_unbind_missing_key_ok(self) -> None:
        """Test that unbind works for non-existent keys."""
        logger = StackLogger()
        logger.unbind("nonexistent")  # Should not raise

    def test_unbind_returns_self(self) -> None:
        """Test that unbind returns self for chaining."""
        logger = StackLogger()
        result = logger.unbind("key")
        assert result is logger

    def test_debug_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test debug logging."""
        with caplog.at_level(logging.DEBUG):
            logger = StackLogger(level="DEBUG")
            logger.debug("debug message")
        assert "debug message" in caplog.text

    def test_info_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test info logging."""
        with caplog.at_level(logging.INFO):
            logger = StackLogger(level="INFO")
            logger.info("info message")
        assert "info message" in caplog.text

    def test_warning_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test warning logging."""
        with caplog.at_level(logging.WARNING):
            logger = StackLogger(level="WARNING")
            logger.warning("warning message")
        assert "warning message" in caplog.text

    def test_error_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test error logging."""
        with caplog.at_level(logging.ERROR):
            logger = StackLogger(level="ERROR")
            logger.error("error message")
        assert "error message" in caplog.text

    def test_critical_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test critical logging."""
        with caplog.at_level(logging.CRITICAL):
            logger = StackLogger(level="CRITICAL")
            logger.critical("critical message")
        assert "critical message" in caplog.text

    def test_exception_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test exception logging with traceback."""
        with caplog.at_level(logging.ERROR):
            logger = StackLogger()
            try:
                raise ValueError("test error")
            except ValueError:
                logger.exception("caught error")
        assert "caught error" in caplog.text

    def test_context_in_message(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that context appears in log message."""
        with caplog.at_level(logging.INFO):
            logger = StackLogger()
            logger.bind(request_id="abc123")
            logger.info("test message")
        assert "request_id=abc123" in caplog.text


class TestStackLoggerStructured:
    """Tests for StackLogger with structlog enabled."""

    @pytest.fixture
    def structured_logger(self) -> StackLogger:
        """Return a structured StackLogger instance."""
        return StackLogger("test_struct", use_structured=True)

    def test_structured_init(self, structured_logger: StackLogger) -> None:
        assert structured_logger.name == "test_struct"
        assert structured_logger._structured

    def test_structured_bind_unbind(self, structured_logger: StackLogger) -> None:
        structured_logger.bind(test_key="test_val")
        assert structured_logger._context["test_key"] == "test_val"

        structured_logger.unbind("test_key")
        assert "test_key" not in structured_logger._context

    def test_structured_logging_methods(self, structured_logger: StackLogger) -> None:
        # Just verifying they don't break.
        # Actual structlog output capture can be tricky without heavily mocking structlog,
        # but calling them gives us coverage.
        structured_logger.debug("debug message", extra="info")
        structured_logger.info("info message", extra="info")
        structured_logger.warning("warning message", extra="info")
        structured_logger.error("error message", extra="info")
        structured_logger.critical("critical message", extra="info")
        try:
            raise ValueError("Test error")
        except ValueError:
            structured_logger.exception("exception message", extra="info")

    def test_setup_logging_structured(self) -> None:
        """Test setup_logging with structlog."""
        setup_logging(use_structured=True)
        # Verify it doesn't break

    def test_get_logger_structured(self) -> None:
        """Test get_logger with structlog."""
        logger = get_logger("test", use_structured=True)
        assert logger._structured


class TestMaskSensitiveDataProcessor:
    """Tests for mask_sensitive_data_processor."""

    def test_mask_sensitive_data(self) -> None:
        event_dict = {
            "message": "User login",
            "password": "my_secret_password",
            "API_KEY": "12345ABC",
            "user_token": "tokenStringABC",
            "safe_field": "safe_value",
            "Authorization": "Bearer 1234",
        }

        result = mask_sensitive_data_processor(None, "info", event_dict)

        assert result["message"] == "User login"
        assert result["password"] == REDACTED_VALUE
        assert result["API_KEY"] == REDACTED_VALUE
        assert result["user_token"] == REDACTED_VALUE
        assert result["Authorization"] == REDACTED_VALUE
        assert result["safe_field"] == "safe_value"


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_stack_logger(self) -> None:
        """Test that get_logger returns StackLogger instance."""
        logger = get_logger()
        assert isinstance(logger, StackLogger)

    def test_custom_name(self) -> None:
        """Test logger with custom name."""
        logger = get_logger(name="custom")
        assert logger.name == "custom"

    def test_custom_level(self) -> None:
        """Test logger with custom level."""
        logger = get_logger(level="DEBUG")
        assert logger.level == "DEBUG"


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_with_defaults(self) -> None:
        """Test setup_logging with default parameters."""
        setup_logging()
        # Should not raise

    def test_setup_with_debug_level(self) -> None:
        """Test setup with DEBUG level."""
        setup_logging(level="DEBUG")

    def test_setup_with_simple_format(self) -> None:
        """Test setup with simple format."""
        setup_logging(format_type="simple")

    def test_setup_with_json_format(self) -> None:
        """Test setup with JSON format."""
        setup_logging(format_type="json")

    def test_setup_with_detailed_format(self) -> None:
        """Test setup with detailed format."""
        setup_logging(format_type="detailed")

    def test_setup_with_log_file(self, tmp_path: Path) -> None:
        """Test setup with a log file."""
        log_file = tmp_path / "test.log"
        setup_logging(log_file=str(log_file))
        assert log_file.exists()


class TestLogOperation:
    """Tests for log_operation context manager."""

    def test_expected_exceptions_handling(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that only expected_exceptions are caught and logged as failures."""

        class ExpectedError(Exception):
            pass

        class UnexpectedError(Exception):
            pass

        # 1. Expected exception should be caught, logged as failure, and re-raised
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ExpectedError):
                with log_operation("expected_op", expected_exceptions=ExpectedError):
                    raise ExpectedError("This is expected")

        assert "Failed: expected_op" in caplog.text

        caplog.clear()

        # 2. Unexpected exception should NOT be caught by log_operation and thus not logged as failure
        with caplog.at_level(logging.ERROR):
            with pytest.raises(UnexpectedError):
                with log_operation("unexpected_op", expected_exceptions=ExpectedError):
                    raise UnexpectedError("This is unexpected")

        assert "Failed: unexpected_op" not in caplog.text

    def test_logs_start_and_end(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that operation start and end are logged."""
        with caplog.at_level(logging.INFO):
            with log_operation("test_operation"):
                pass
        assert "Starting: test_operation" in caplog.text
        assert "Completed: test_operation" in caplog.text

    def test_logs_duration(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that duration is logged."""
        with caplog.at_level(logging.INFO):
            with log_operation("test_operation"):
                pass
        assert "duration_seconds" in caplog.text

    def test_custom_logger(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that log_operation uses the provided custom logger."""
        custom_logger = get_logger("custom_op_logger")
        with caplog.at_level(logging.INFO):
            with log_operation("custom_op", logger=custom_logger):
                pass
        assert "custom_op" in caplog.text
        assert "custom_op_logger" in caplog.text

    def test_logs_exception_on_failure(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that exception is logged on failure."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                with log_operation("failing_operation"):
                    raise ValueError("test error")
        assert "Failed: failing_operation" in caplog.text

    def test_reraises_exception(self) -> None:
        """Test that exceptions are re-raised."""
        with pytest.raises(ValueError, match="original"):
            with log_operation("test"):
                raise ValueError("original")

    def test_expected_exceptions_caught_and_logged(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that specified expected exceptions are caught and logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError, match="expected"):
                with log_operation("test_expected", expected_exceptions=ValueError):
                    raise ValueError("expected")
        assert "Failed: test_expected" in caplog.text

    def test_unexpected_exceptions_bypass_catch(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that unexpected exceptions bypass the catch block and are not logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError, match="unexpected"):
                with log_operation("test_unexpected", expected_exceptions=ValueError):
                    raise TypeError("unexpected")
        assert "Failed: test_unexpected" not in caplog.text


class TestFormatConstants:
    """Tests for format string constants."""

    def test_default_format_has_required_fields(self) -> None:
        """Test DEFAULT_FORMAT has required placeholders."""
        assert "%(asctime)s" in DEFAULT_FORMAT
        assert "%(levelname)" in DEFAULT_FORMAT
        assert "%(name)s" in DEFAULT_FORMAT
        assert "%(message)s" in DEFAULT_FORMAT

    def test_json_format_is_valid_json_template(self) -> None:
        """Test JSON_FORMAT produces valid JSON structure."""
        assert "timestamp" in JSON_FORMAT
        assert "level" in JSON_FORMAT
        assert "logger" in JSON_FORMAT
        assert "message" in JSON_FORMAT


class TestCorrelationId:
    """Tests for correlation_id contextvars."""

    def test_correlation_id_processor_with_id(self) -> None:
        """Test processor injects ID when set."""
        set_correlation_id("injected-id")

        event_dict: dict[str, Any] = {"message": "test msg"}
        new_dict = correlation_id_processor(None, "info", event_dict)

        assert new_dict["correlation_id"] == "injected-id"
        assert new_dict["message"] == "test msg"

        set_correlation_id(None)

    def test_correlation_id_processor_without_id(self) -> None:
        """Test processor does not inject ID when not set."""
        set_correlation_id(None)

        event_dict: dict[str, Any] = {"message": "test msg"}
        new_dict = correlation_id_processor(None, "info", event_dict)

        assert "correlation_id" not in new_dict
        assert new_dict["message"] == "test msg"
