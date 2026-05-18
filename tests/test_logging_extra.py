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


# Migrated from tests/test_fuzz_logging_redact_operations.py
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.utils.logging import _redact_dict


@given(
    value=st.dictionaries(
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.none(),
            st.booleans(),
            st.dates(),
            st.datetimes(),
        ),
        st.one_of(
            st.text(),
            st.integers(),
            st.floats(),
            st.none(),
            st.booleans(),
            st.dates(),
            st.datetimes(),
        ),
    )
)
@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_logging_redact_fuzz_redact_dict_extreme_keys(value):
    """Bombard _redact_dict with extreme, non-string keys to test resilience.

    Keys generated include None, integers, floats, booleans, dates, and datetimes.
    The function should gracefully skip non-string keys instead of raising a TypeError.
    """
    # We need a copy because hypothesis strategies give us read-only views sometimes,
    # or we might mutate the input dict and break hypothesis' assumptions if not careful,
    # but _redact_dict takes a MutableMapping and mutates it in place.
    # Actually hypothesis gives new dicts for each example.
    mutable_value = dict(value)
    _redact_dict(mutable_value)


# Migrated from tests/test_v034_logging_coverage_operations.py


def test_v034_logging_coverage_coverage():
    from taipanstack.utils import logging as my_logging

    # Temporarily set regex to None to hit the branch
    old_regex = my_logging._SENSITIVE_KEY_REGEX
    my_logging._SENSITIVE_KEY_REGEX = None

    try:
        res = mask_sensitive_data_processor(None, None, {"test": "val"})
        assert res == {"test": "val"}

        # Hitting _is_sensitive(key, None)
        assert my_logging._is_sensitive("any", None) is False
    finally:
        my_logging._SENSITIVE_KEY_REGEX = old_regex


if __name__ == "__main__":
    test_v034_logging_coverage_coverage()


# Migrated from tests/test_v034_logging_mask_operations.py
"""Tests for the mask_sensitive_data_processor structlog processor."""

from taipanstack.utils.logging import SENSITIVE_KEY_PATTERNS

# ---------------------------------------------------------------------------
# Unit tests: processor function directly
# ---------------------------------------------------------------------------


class TestMaskSensitiveDataProcessor:
    """Direct unit tests for mask_sensitive_data_processor."""

    def test_v034_logging_mask_password_key_is_redacted(self) -> None:
        """Value under a 'password' key is replaced with REDACTED_VALUE."""
        event_dict = {"event": "user_login", "password": "hunter2"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["password"] == REDACTED_VALUE
        assert result["event"] == "user_login"

    def test_v034_logging_mask_secret_key_is_redacted(self) -> None:
        """Value under a 'secret' key is replaced with REDACTED_VALUE."""
        event_dict = {"event": "init", "secret": "mysecretvalue"}
        result = mask_sensitive_data_processor(None, "warning", event_dict)
        assert result["secret"] == REDACTED_VALUE

    def test_v034_logging_mask_token_key_is_redacted(self) -> None:
        """Value under a 'token' key is replaced with REDACTED_VALUE."""
        event_dict = {"token": "Bearer abc123", "event": "auth"}
        result = mask_sensitive_data_processor(None, "debug", event_dict)
        assert result["token"] == REDACTED_VALUE

    def test_v034_logging_mask_authorization_key_is_redacted(self) -> None:
        """Value under an 'authorization' key is replaced with REDACTED_VALUE."""
        event_dict = {"authorization": "Basic dXNlcjpwYXNz", "event": "request"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["authorization"] == REDACTED_VALUE

    def test_v034_logging_mask_api_key_is_redacted(self) -> None:
        """Value under an 'api_key' key is replaced with REDACTED_VALUE."""
        event_dict = {"api_key": "sk-super-secret", "event": "api_call"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["api_key"] == REDACTED_VALUE

    def test_v034_logging_mask_case_insensitive_matching_password(
        self,
    ) -> None:
        """Keys containing 'PASSWORD' (uppercase) are also redacted."""
        event_dict = {"USER_PASSWORD": "p4ssw0rd", "event": "test"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["USER_PASSWORD"] == REDACTED_VALUE

    def test_v034_logging_mask_case_insensitive_matching_token(self) -> None:
        """Keys containing 'TOKEN' (mixed case) are also redacted."""
        event_dict = {"OAuth_Token": "xyz", "event": "test"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["OAuth_Token"] == REDACTED_VALUE

    def test_v034_logging_mask_case_insensitive_matching_secret(self) -> None:
        """Keys containing 'Secret' (title case) are also redacted."""
        event_dict = {"ClientSecret": "very-secret", "event": "test"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["ClientSecret"] == REDACTED_VALUE

    def test_v034_logging_mask_partial_key_match_is_redacted(self) -> None:
        """Keys that contain a sensitive substring anywhere are redacted."""
        event_dict = {"db_password_hash": "xxxx", "event": "test"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["db_password_hash"] == REDACTED_VALUE

    def test_v034_logging_mask_non_sensitive_keys_are_untouched(self) -> None:
        """Keys not matching any sensitive pattern are left as-is."""
        event_dict = {
            "event": "startup",
            "user": "alice",
            "request_id": "req-001",
            "duration": 1.23,
        }
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["event"] == "startup"
        assert result["user"] == "alice"
        assert result["request_id"] == "req-001"
        assert result["duration"] == 1.23

    def test_v034_logging_mask_empty_event_dict_is_returned_unchanged(
        self,
    ) -> None:
        """An empty event dict passes through without error."""
        event_dict: dict[str, object] = {}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result == {}

    def test_v034_logging_mask_returns_same_dict_object(self) -> None:
        """Processor returns the same event_dict object (in-place mutation)."""
        event_dict = {"event": "test", "password": "secret"}
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result is event_dict

    def test_v034_logging_mask_multiple_sensitive_keys_all_redacted(
        self,
    ) -> None:
        """Multiple sensitive keys in one event dict are all redacted."""
        event_dict = {
            "event": "multi",
            "password": "pass1",
            "token": "tok1",
            "api_key": "key1",
            "name": "alice",
        }
        result = mask_sensitive_data_processor(None, "info", event_dict)
        assert result["password"] == REDACTED_VALUE
        assert result["token"] == REDACTED_VALUE
        assert result["api_key"] == REDACTED_VALUE
        assert result["name"] == "alice"

    def test_v034_logging_mask_logger_and_method_args_ignored(self) -> None:
        """Processor ignores the logger and method arguments correctly."""
        # Both None and real-looking values are acceptable; result is unchanged
        event_dict = {"event": "check", "secret": "val"}
        result1 = mask_sensitive_data_processor(None, "info", event_dict)
        event_dict2 = {"event": "check2", "secret": "val2"}
        result2 = mask_sensitive_data_processor(object(), "warning", event_dict2)
        assert result1["secret"] == REDACTED_VALUE
        assert result2["secret"] == REDACTED_VALUE


class TestSensitiveKeyPatternsConstant:
    """Tests for the SENSITIVE_KEY_PATTERNS constant."""

    def test_v034_logging_mask_contains_patterns(self) -> None:
        """SENSITIVE_KEY_PATTERNS includes all required substrings."""
        required = {"password", "secret", "token", "authorization", "api_key"}
        assert required.issubset(set(SENSITIVE_KEY_PATTERNS))

    def test_v034_logging_mask_patterns_are_lowercase(self) -> None:
        """All SENSITIVE_KEY_PATTERNS entries are lower-case for case-folding."""
        for pattern in SENSITIVE_KEY_PATTERNS:
            assert pattern == pattern.lower(), f"Pattern '{pattern}' is not lowercase"


# ---------------------------------------------------------------------------
# Integration test: processor wired into structlog pipeline
# ---------------------------------------------------------------------------


class TestMaskSensitiveDataProcessorStructlogIntegration:
    """Integration tests: processor wired into a real structlog configuration."""

    def test_v034_logging_mask_structlog_pipeline_masks_password(self) -> None:
        """Password value is masked when processor is in the structlog chain."""
        import io

        import structlog

        output = io.StringIO()

        structlog.configure(
            processors=[
                mask_sensitive_data_processor,
                structlog.dev.ConsoleRenderer(colors=False),
            ],
            logger_factory=structlog.PrintLoggerFactory(file=output),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=False,
        )

        log = structlog.get_logger()
        log.info("user_login", password="hunter2", username="alice")

        captured = output.getvalue()
        assert "hunter2" not in captured, "Raw password must not appear in log output"
        assert REDACTED_VALUE in captured, "Redacted sentinel must appear in log output"

    def test_v034_logging_mask_structlog_pipeline_masks_authorization_header(
        self,
    ) -> None:
        """Authorization header value is masked in the structlog pipeline."""
        import io

        import structlog

        output = io.StringIO()

        structlog.configure(
            processors=[
                mask_sensitive_data_processor,
                structlog.dev.ConsoleRenderer(colors=False),
            ],
            logger_factory=structlog.PrintLoggerFactory(file=output),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=False,
        )

        log = structlog.get_logger()
        log.warning("http_request", authorization="Bearer secret-jwt-token")

        captured = output.getvalue()
        assert "secret-jwt-token" not in captured
        assert REDACTED_VALUE in captured

    def test_v034_logging_mask_structlog_pipeline_preserves_non_sensitive_fields(
        self,
    ) -> None:
        """Non-sensitive fields are preserved untouched in the pipeline."""
        import io

        import structlog

        output = io.StringIO()

        structlog.configure(
            processors=[
                mask_sensitive_data_processor,
                structlog.dev.ConsoleRenderer(colors=False),
            ],
            logger_factory=structlog.PrintLoggerFactory(file=output),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=False,
        )

        log = structlog.get_logger()
        log.info("startup", service="api", version="0.3.4")

        captured = output.getvalue()
        assert "api" in captured
        assert "0.3.4" in captured

    def test_v034_logging_mask_structlog_pipeline_masks_api_key(self) -> None:
        """API key value is masked when wired through the structlog pipeline."""
        import io

        import structlog

        output = io.StringIO()

        structlog.configure(
            processors=[
                mask_sensitive_data_processor,
                structlog.dev.ConsoleRenderer(colors=False),
            ],
            logger_factory=structlog.PrintLoggerFactory(file=output),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=False,
        )

        log = structlog.get_logger()
        log.info("api_request", api_key="sk-abc-xyz-123")

        captured = output.getvalue()
        assert "sk-abc-xyz-123" not in captured
        assert REDACTED_VALUE in captured

    def test_v034_logging_mask_structlog_pipeline_masks_token(self) -> None:
        """Token value is masked when wired through the structlog pipeline."""
        import io

        import structlog

        output = io.StringIO()

        structlog.configure(
            processors=[
                mask_sensitive_data_processor,
                structlog.dev.ConsoleRenderer(colors=False),
            ],
            logger_factory=structlog.PrintLoggerFactory(file=output),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=False,
        )

        log = structlog.get_logger()
        log.debug("token_refresh", token="eyJhbGciOiJIUzI1NiJ9.payload")

        captured = output.getvalue()
        assert "eyJhbGciOiJIUzI1NiJ9.payload" not in captured
        assert REDACTED_VALUE in captured
