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

    def test_utils_logging_logging_no_structlog_standard_expected(self) -> None:
        """Test fallback when structlog is not installed."""
        import importlib.util
        from unittest import mock

        with mock.patch.dict("sys.modules", {"structlog": None}):
            spec = importlib.util.find_spec("taipanstack.utils.logging")
            module = importlib.util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(module)  # type: ignore
            assert module.HAS_STRUCTLOG is False

    def test_utils_logging_init_with_defaults_standard_expected(self) -> None:
        """Test logger initialization with defaults."""
        logger = StackLogger()
        assert logger.name == "stack"
        assert logger.level == "INFO"

    def test_utils_logging_init_with_custom_name_standard_expected(self) -> None:
        """Test logger with custom name."""
        logger = StackLogger(name="my_module")
        assert logger.name == "my_module"

    def test_utils_logging_init_with_custom_level_standard_expected(self) -> None:
        """Test logger with custom level."""
        logger = StackLogger(level="DEBUG")
        assert logger.level == "DEBUG"

    def test_utils_logging_bind_adds_context_standard_expected(self) -> None:
        """Test that bind adds context."""
        logger = StackLogger()
        logger.bind(request_id="123", user="test")
        assert logger._context["request_id"] == "123"
        assert logger._context["user"] == "test"

    def test_utils_logging_bind_returns_self_standard_expected(self) -> None:
        """Test that bind returns self for chaining."""
        logger = StackLogger()
        result = logger.bind(key="value")
        assert result is logger

    def test_utils_logging_unbind_removes_context_standard_expected(self) -> None:
        """Test that unbind removes context keys."""
        logger = StackLogger()
        logger.bind(key1="value1", key2="value2")
        logger.unbind("key1")
        assert "key1" not in logger._context
        assert "key2" in logger._context

    def test_utils_logging_unbind_missing_key_ok_standard_expected(self) -> None:
        """Test that unbind works for non-existent keys."""
        logger = StackLogger()
        logger.unbind("nonexistent")  # Should not raise

    def test_utils_logging_unbind_returns_self_standard_expected(self) -> None:
        """Test that unbind returns self for chaining."""
        logger = StackLogger()
        result = logger.unbind("key")
        assert result is logger

    def test_utils_logging_debug_logging_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test debug logging."""
        with caplog.at_level(logging.DEBUG):
            logger = StackLogger(level="DEBUG")
            logger.debug("debug message")
        assert "debug message" in caplog.text

    def test_utils_logging_info_logging_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test info logging."""
        with caplog.at_level(logging.INFO):
            logger = StackLogger(level="INFO")
            logger.info("info message")
        assert "info message" in caplog.text

    def test_utils_logging_warning_logging_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test warning logging."""
        with caplog.at_level(logging.WARNING):
            logger = StackLogger(level="WARNING")
            logger.warning("warning message")
        assert "warning message" in caplog.text

    def test_utils_logging_error_logging_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test error logging."""
        with caplog.at_level(logging.ERROR):
            logger = StackLogger(level="ERROR")
            logger.error("error message")
        assert "error message" in caplog.text

    def test_utils_logging_critical_logging_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test critical logging."""
        with caplog.at_level(logging.CRITICAL):
            logger = StackLogger(level="CRITICAL")
            logger.critical("critical message")
        assert "critical message" in caplog.text

    def test_utils_logging_exception_logging_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test exception logging with traceback."""
        with caplog.at_level(logging.ERROR):
            logger = StackLogger()
            try:
                raise ValueError("test error")
            except ValueError:
                logger.exception("caught error")
        assert "caught error" in caplog.text

    def test_utils_logging_context_in_message_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
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

    def test_utils_logging_structured_init_standard_expected(
        self, structured_logger: StackLogger
    ) -> None:
        assert structured_logger.name == "test_struct"
        assert structured_logger._structured

    def test_utils_logging_structured_bind_unbind_standard_expected(
        self, structured_logger: StackLogger
    ) -> None:
        structured_logger.bind(test_key="test_val")
        assert structured_logger._context["test_key"] == "test_val"

        structured_logger.unbind("test_key")
        assert "test_key" not in structured_logger._context

    def test_utils_logging_structured_logging_methods_standard_expected(
        self, structured_logger: StackLogger
    ) -> None:
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

    def test_utils_logging_setup_logging_structured_standard_expected(self) -> None:
        """Test setup_logging with structlog."""
        setup_logging(use_structured=True)
        # Verify it doesn't break

    def test_utils_logging_get_logger_structured_standard_expected(self) -> None:
        """Test get_logger with structlog."""
        logger = get_logger("test", use_structured=True)
        assert logger._structured


class TestMaskSensitiveDataProcessor:
    """Tests for mask_sensitive_data_processor."""

    def test_utils_logging_mask_sensitive_data_standard_expected(self) -> None:
        event_dict = {
            "message": "User login",
            "password": "my_secret_password",
            "API_KEY": "12345ABC",
            "user_token": "tokenStringABC",
            "safe_field": "safe_value",
            "Authorization": "Bearer 1234",
            "nested_data": {
                "password": "hidden_password",
                "normal": "value",
            },
        }

        result = mask_sensitive_data_processor(None, "info", event_dict)

        assert result["message"] == "User login"
        assert result["password"] == REDACTED_VALUE
        assert result["API_KEY"] == REDACTED_VALUE
        assert result["user_token"] == REDACTED_VALUE
        assert result["Authorization"] == REDACTED_VALUE
        assert result["safe_field"] == "safe_value"
        assert isinstance(result["nested_data"], dict)
        assert result["nested_data"]["password"] == REDACTED_VALUE
        assert result["nested_data"]["normal"] == "value"


class TestGetLogger:
    """Tests for get_logger function."""

    def test_utils_logging_returns_stack_logger_standard_expected(self) -> None:
        """Test that get_logger returns StackLogger instance."""
        logger = get_logger()
        assert isinstance(logger, StackLogger)

    def test_utils_logging_custom_name_standard_expected(self) -> None:
        """Test logger with custom name."""
        logger = get_logger(name="custom")
        assert logger.name == "custom"

    def test_utils_logging_custom_level_standard_expected(self) -> None:
        """Test logger with custom level."""
        logger = get_logger(level="DEBUG")
        assert logger.level == "DEBUG"


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_utils_logging_setup_with_defaults_standard_expected(self) -> None:
        """Test setup_logging with default parameters."""
        setup_logging()
        # Should not raise

    def test_utils_logging_setup_with_debug_level_standard_expected(self) -> None:
        """Test setup with DEBUG level."""
        setup_logging(level="DEBUG")

    def test_utils_logging_setup_with_simple_format_standard_expected(self) -> None:
        """Test setup with simple format."""
        setup_logging(format_type="simple")

    def test_utils_logging_setup_with_json_format_standard_expected(self) -> None:
        """Test setup with JSON format."""
        setup_logging(format_type="json")

    def test_utils_logging_setup_with_detailed_format_standard_expected(self) -> None:
        """Test setup with detailed format."""
        setup_logging(format_type="detailed")

    def test_utils_logging_setup_with_log_file_standard_expected(
        self, tmp_path: Path
    ) -> None:
        """Test setup with a log file."""
        log_file = tmp_path / "test.log"
        setup_logging(log_file=str(log_file))
        assert log_file.exists()


class TestLogOperation:
    """Tests for log_operation context manager."""

    def test_utils_logging_exceptions_handling_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that only expected_exceptions are caught and logged as failures."""

        class ExpectedError(Exception): ...

        class UnexpectedError(Exception): ...

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

    def test_utils_logging_logs_start_and_end_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that operation start and end are logged."""
        with caplog.at_level(logging.INFO):
            with log_operation("test_operation"):
                assert True
        assert "Starting: test_operation" in caplog.text
        assert "Completed: test_operation" in caplog.text

    def test_utils_logging_logs_duration_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that duration is logged."""
        with caplog.at_level(logging.INFO):
            with log_operation("test_operation"):
                assert True
        assert "duration_seconds" in caplog.text

    def test_utils_logging_custom_logger_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that log_operation uses the provided custom logger."""
        custom_logger = get_logger("custom_op_logger")
        with caplog.at_level(logging.INFO):
            with log_operation("custom_op", logger=custom_logger):
                assert True
        assert "custom_op" in caplog.text
        assert "custom_op_logger" in caplog.text

    def test_utils_logging_logs_exception_on_failure(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that exception is logged on failure."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                with log_operation("failing_operation"):
                    raise ValueError("test error")
        assert "Failed: failing_operation" in caplog.text

    def test_utils_logging_reraises_exception_standard_expected(self) -> None:
        """Test that exceptions are re-raised."""
        with pytest.raises(ValueError, match="original"):
            with log_operation("test"):
                raise ValueError("original")

    def test_utils_logging_exceptions_caught_and_logged_standard_expected(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that specified expected exceptions are caught and logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError, match="expected"):
                with log_operation("test_expected", expected_exceptions=ValueError):
                    raise ValueError("expected")
        assert "Failed: test_expected" in caplog.text

    def test_utils_logging_unexpected_exceptions_bypass_catch_standard_expected(
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

    def test_utils_logging_default_format_has_required_fields_standard_expected(
        self,
    ) -> None:
        """Test DEFAULT_FORMAT has required placeholders."""
        assert "%(asctime)s" in DEFAULT_FORMAT
        assert "%(levelname)" in DEFAULT_FORMAT
        assert "%(name)s" in DEFAULT_FORMAT
        assert "%(message)s" in DEFAULT_FORMAT

    def test_utils_logging_json_format_is_valid_json_template_standard_expected(
        self,
    ) -> None:
        """Test JSON_FORMAT produces valid JSON structure."""
        assert "timestamp" in JSON_FORMAT
        assert "level" in JSON_FORMAT
        assert "logger" in JSON_FORMAT
        assert "message" in JSON_FORMAT


class TestCorrelationId:
    """Tests for correlation_id contextvars."""

    def test_utils_logging_correlation_id_processor_with_id_standard_expected(
        self,
    ) -> None:
        """Test processor injects ID when set."""
        set_correlation_id("injected-id")

        event_dict: dict[str, Any] = {"message": "test msg"}
        new_dict = correlation_id_processor(None, "info", event_dict)

        assert new_dict["correlation_id"] == "injected-id"
        assert new_dict["message"] == "test msg"

        set_correlation_id(None)

    def test_utils_logging_correlation_id_processor_without_id_standard_expected(
        self,
    ) -> None:
        """Test processor does not inject ID when not set."""
        set_correlation_id(None)

        event_dict: dict[str, Any] = {"message": "test msg"}
        new_dict = correlation_id_processor(None, "info", event_dict)

        assert "correlation_id" not in new_dict
        assert new_dict["message"] == "test msg"


def test_utils_logging_is_sensitive_regex_none_returns_false_standard_expected() -> (
    None
):
    """_is_sensitive returns False when regex is None."""
    from taipanstack.utils.logging import _is_sensitive

    assert _is_sensitive("password", None) is False


def test_utils_logging_redact_custom_mutable_mapping_standard_expected() -> None:
    """Test _redact with a custom MutableMapping that is not a dict."""
    from collections.abc import Iterator, MutableMapping

    from taipanstack.utils.logging import _redact

    class CustomMapping(MutableMapping[Any, Any]):
        def __init__(self, data: dict[Any, Any]):
            self._data = data

        def __getitem__(self, key: Any) -> Any:
            return self._data[key]

        def __setitem__(self, key: Any, value: Any) -> None:
            self._data[key] = value

        def __delitem__(self, key: Any) -> None:
            del self._data[key]

        def __iter__(self) -> Iterator[Any]:
            return iter(self._data)

        def __len__(self) -> int:
            return len(self._data)

    custom = CustomMapping({"password": "secret", "safe": "value"})
    redacted = _redact(custom)
    assert isinstance(redacted, dict)
    assert redacted["password"] == REDACTED_VALUE
    assert redacted["safe"] == "value"
