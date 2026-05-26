from unittest.mock import patch

from taipanstack.utils.logging import (
    REDACTED_VALUE,
    StackLogger,
    mask_sensitive_data_processor,
)


def test_logging_extra_mask_sensitive_data_processor_none_regex():
    """Test mask_sensitive_data_processor when _SENSITIVE_KEY_REGEX is None."""
    with patch("taipanstack.utils.logging._SENSITIVE_KEY_REGEX", None):
        event_dict = {"password": "secret"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["password"] == "secret"


def test_logging_extra_format_message_none_regex():
    """Test _format_message when _SENSITIVE_KEY_REGEX is None."""
    with patch("taipanstack.utils.logging._SENSITIVE_KEY_REGEX", None):
        logger = StackLogger()
        msg = logger._format_message("test", password="secret")
        assert "password=secret" in msg


def test_logging_extra_format_message_masking():
    """Test _format_message masking logic."""
    logger = StackLogger()
    msg = logger._format_message("test", password="secret")
    assert f"password={REDACTED_VALUE}" in msg
    assert "password=secret" not in msg


def test_logging_extra_format_message_no_kwargs_with_context():
    """Test _format_message when kwargs are empty but _context is populated."""
    logger = StackLogger()
    logger.bind(context_key="context_value")
    msg = logger._format_message("test message")
    assert "test message" in msg
    assert "context_key=context_value" in msg
