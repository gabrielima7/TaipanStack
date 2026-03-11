from unittest.mock import patch

from taipanstack.utils.logging import (
    REDACTED_VALUE,
    StackLogger,
    mask_sensitive_data_processor,
)


def test_mask_sensitive_data_processor_none_regex():
    """Test mask_sensitive_data_processor when _SENSITIVE_KEY_REGEX is None."""
    with patch("taipanstack.utils.logging._SENSITIVE_KEY_REGEX", None):
        event_dict = {"password": "secret"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["password"] == "secret"


def test_format_message_none_regex():
    """Test _format_message when _SENSITIVE_KEY_REGEX is None."""
    with patch("taipanstack.utils.logging._SENSITIVE_KEY_REGEX", None):
        logger = StackLogger()
        msg = logger._format_message("test", password="secret")
        assert "password=secret" in msg


def test_format_message_masking():
    """Test _format_message masking logic."""
    logger = StackLogger()
    msg = logger._format_message("test", password="secret")
    assert f"password={REDACTED_VALUE}" in msg
    assert "password=secret" not in msg
