"""Tests for v0.3.1 edge-case protections and new features.

Covers: TypeError guards, SecurityError edge cases, on_retry callback,
and on_state_change callback.
"""
import time

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState
from taipanstack.resilience.retry import retry
from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_env_variable,
    guard_path_traversal,
)
from taipanstack.security.sanitizers import sanitize_filename, sanitize_string
from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
    validate_url,
)


class TestGuardPathTraversalTypeCheck:
    """Tests for guard_path_traversal input type validation."""

    def test_rejects_int_input_expected(self, tmp_path: object) -> None:
        with pytest.raises(TypeError, match="path must be str or Path, got int"):
            guard_path_traversal(123)

    def test_rejects_none_input_expected(self) -> None:
        with pytest.raises(TypeError, match="got NoneType"):
            guard_path_traversal(None)

    def test_rejects_list_input_expected(self) -> None:
        with pytest.raises(TypeError, match="got list"):
            guard_path_traversal(["/foo"])

class TestGuardCommandInjectionTypeCheck:
    """Tests for guard_command_injection item type validation."""

    def test_rejects_non_string_items_expected(self) -> None:
        with pytest.raises(TypeError, match="got int at index 2"):
            guard_command_injection(["git", "clone", 123])

    def test_rejects_none_item_expected(self) -> None:
        with pytest.raises(TypeError, match="got NoneType at index 0"):
            guard_command_injection([None, "foo"])

class TestGuardEnvVariableEdgeCases:
    """Tests for guard_env_variable edge-case validation."""

    def test_rejects_non_string_name_expected(self) -> None:
        with pytest.raises(TypeError, match="Variable name must be str, got int"):
            guard_env_variable(123)

    def test_rejects_empty_name_expected(self) -> None:
        with pytest.raises(SecurityError, match="empty or whitespace"):
            guard_env_variable("")

    def test_rejects_whitespace_only_name_expected(self) -> None:
        with pytest.raises(SecurityError, match="empty or whitespace"):
            guard_env_variable("   ")

class TestSanitizeStringTypeCheck:
    """Tests for sanitize_string input type validation."""

    def test_v031_features_rejects_none_expected(self) -> None:
        with pytest.raises(TypeError, match="value must be str, got NoneType"):
            sanitize_string(None)

    def test_v031_features_rejects_int_expected(self) -> None:
        with pytest.raises(TypeError, match="got int"):
            sanitize_string(42)

class TestSanitizeFilenameTypeCheck:
    """Tests for sanitize_filename input type validation."""

    def test_v031_features_rejects_none_expected(self) -> None:
        with pytest.raises(TypeError, match="filename must be str, got NoneType"):
            sanitize_filename(None)

    def test_v031_features_rejects_int_expected(self) -> None:
        with pytest.raises(TypeError, match="got int"):
            sanitize_filename(123)

class TestValidatorTypeChecks:
    """Tests for TypeError validation in validators."""

    def test_validate_project_name_rejects_int_expected(self) -> None:
        with pytest.raises(TypeError, match="Project name must be str, got int"):
            validate_project_name(123)

    def test_validate_python_version_rejects_float_expected(self) -> None:
        with pytest.raises(TypeError, match="Version must be str, got float"):
            validate_python_version(3.12)

    def test_validate_email_rejects_int_expected(self) -> None:
        with pytest.raises(TypeError, match="Email must be str, got int"):
            validate_email(42)

    def test_validate_url_rejects_none_expected(self) -> None:
        with pytest.raises(TypeError, match="URL must be str, got NoneType"):
            validate_url(None)

class TestOnRetryCallback:
    """Tests for the on_retry callback in retry decorator."""

    def test_on_retry_callback_invoked_expected(self) -> None:
        """Verify on_retry is called with correct arguments on each retry."""
        callback_calls: list[tuple[int, int, Exception, float]] = []

        def capture_retry(attempt: int, max_attempts: int, exc: Exception, delay: float) -> None:
            callback_calls.append((attempt, max_attempts, exc, delay))
        call_count = 0

        @retry(max_attempts=3, initial_delay=0.01, on=(ValueError,), on_retry=capture_retry)
        def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("fail")
            return "ok"
        result = flaky()
        assert result == "ok"
        assert len(callback_calls) == 2
        assert callback_calls[0][0] == 1
        assert callback_calls[0][1] == 3
        assert isinstance(callback_calls[0][2], ValueError)
        assert callback_calls[0][3] > 0

class TestOnStateChangeCallback:
    """Tests for the on_state_change callback in CircuitBreaker."""

    def test_callback_on_closed_to_open_expected(self) -> None:
        """Verify callback fires when circuit opens after failures."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        def capture(old: CircuitState, new: CircuitState) -> None:
            transitions.append((old, new))
        breaker = CircuitBreaker(failure_threshold=2, timeout=0.1, name="test_cb", on_state_change=capture)

        @breaker
        def failing() -> str:
            raise RuntimeError("boom")
        for _ in range(2):
            with pytest.raises(RuntimeError):
                failing()
        assert len(transitions) == 1
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)

    def test_callback_on_full_lifecycle_expected(self) -> None:
        """Verify callback fires for CLOSED→OPEN→HALF_OPEN→CLOSED."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        def capture(old: CircuitState, new: CircuitState) -> None:
            transitions.append((old, new))
        breaker = CircuitBreaker(failure_threshold=2, success_threshold=1, timeout=0.05, name="lifecycle", on_state_change=capture)
        call_should_fail = True

        @breaker
        def service() -> str:
            if call_should_fail:
                raise RuntimeError("down")
            return "ok"
        for _ in range(2):
            with pytest.raises(RuntimeError):
                service()
        time.sleep(0.1)
        call_should_fail = False
        result = service()
        assert result == "ok"
        assert len(transitions) == 3
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)
        assert transitions[1] == (CircuitState.OPEN, CircuitState.HALF_OPEN)
        assert transitions[2] == (CircuitState.HALF_OPEN, CircuitState.CLOSED)
