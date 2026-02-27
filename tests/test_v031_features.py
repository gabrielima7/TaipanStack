"""Tests for v0.3.1 edge-case protections and new features.

Covers: TypeError guards, SecurityError edge cases, on_retry callback,
and on_state_change callback.
"""

from __future__ import annotations

import time

import pytest

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
from taipanstack.utils.circuit_breaker import CircuitBreaker, CircuitState
from taipanstack.utils.retry import retry

# ---------- guards.py ----------


class TestGuardPathTraversalTypeCheck:
    """Tests for guard_path_traversal input type validation."""

    def test_rejects_int_input(self, tmp_path: object) -> None:
        with pytest.raises(TypeError, match="path must be str or Path, got int"):
            guard_path_traversal(123)  # type: ignore[arg-type]

    def test_rejects_none_input(self) -> None:
        with pytest.raises(TypeError, match="got NoneType"):
            guard_path_traversal(None)  # type: ignore[arg-type]

    def test_rejects_list_input(self) -> None:
        with pytest.raises(TypeError, match="got list"):
            guard_path_traversal(["/foo"])  # type: ignore[arg-type]


class TestGuardCommandInjectionTypeCheck:
    """Tests for guard_command_injection item type validation."""

    def test_rejects_non_string_items(self) -> None:
        with pytest.raises(TypeError, match="got int at index 2"):
            guard_command_injection(["git", "clone", 123])  # type: ignore[list-item]

    def test_rejects_none_item(self) -> None:
        with pytest.raises(TypeError, match="got NoneType at index 0"):
            guard_command_injection([None, "foo"])  # type: ignore[list-item]


class TestGuardEnvVariableEdgeCases:
    """Tests for guard_env_variable edge-case validation."""

    def test_rejects_non_string_name(self) -> None:
        with pytest.raises(TypeError, match="Variable name must be str, got int"):
            guard_env_variable(123)  # type: ignore[arg-type]

    def test_rejects_empty_name(self) -> None:
        with pytest.raises(SecurityError, match="empty or whitespace"):
            guard_env_variable("")

    def test_rejects_whitespace_only_name(self) -> None:
        with pytest.raises(SecurityError, match="empty or whitespace"):
            guard_env_variable("   ")


# ---------- sanitizers.py ----------


class TestSanitizeStringTypeCheck:
    """Tests for sanitize_string input type validation."""

    def test_rejects_none(self) -> None:
        with pytest.raises(TypeError, match="value must be str, got NoneType"):
            sanitize_string(None)  # type: ignore[arg-type]

    def test_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="got int"):
            sanitize_string(42)  # type: ignore[arg-type]


class TestSanitizeFilenameTypeCheck:
    """Tests for sanitize_filename input type validation."""

    def test_rejects_none(self) -> None:
        with pytest.raises(TypeError, match="filename must be str, got NoneType"):
            sanitize_filename(None)  # type: ignore[arg-type]

    def test_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="got int"):
            sanitize_filename(123)  # type: ignore[arg-type]


# ---------- validators.py ----------


class TestValidatorTypeChecks:
    """Tests for TypeError validation in validators."""

    def test_validate_project_name_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="Project name must be str, got int"):
            validate_project_name(123)  # type: ignore[arg-type]

    def test_validate_python_version_rejects_float(self) -> None:
        with pytest.raises(TypeError, match="Version must be str, got float"):
            validate_python_version(3.12)  # type: ignore[arg-type]

    def test_validate_email_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="Email must be str, got int"):
            validate_email(42)  # type: ignore[arg-type]

    def test_validate_url_rejects_none(self) -> None:
        with pytest.raises(TypeError, match="URL must be str, got NoneType"):
            validate_url(None)  # type: ignore[arg-type]


# ---------- retry.py on_retry callback ----------


class TestOnRetryCallback:
    """Tests for the on_retry callback in retry decorator."""

    def test_on_retry_callback_invoked(self) -> None:
        """Verify on_retry is called with correct arguments on each retry."""
        callback_calls: list[tuple[int, int, Exception, float]] = []

        def capture_retry(
            attempt: int, max_attempts: int, exc: Exception, delay: float
        ) -> None:
            callback_calls.append((attempt, max_attempts, exc, delay))

        call_count = 0

        @retry(
            max_attempts=3,
            initial_delay=0.01,
            on=(ValueError,),
            on_retry=capture_retry,
        )
        def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("fail")
            return "ok"

        result = flaky()
        assert result == "ok"
        assert len(callback_calls) == 2  # 2 retries before success
        assert callback_calls[0][0] == 1  # first attempt
        assert callback_calls[0][1] == 3  # max_attempts
        assert isinstance(callback_calls[0][2], ValueError)
        assert callback_calls[0][3] > 0  # delay > 0


# ---------- circuit_breaker.py on_state_change callback ----------


class TestOnStateChangeCallback:
    """Tests for the on_state_change callback in CircuitBreaker."""

    def test_callback_on_closed_to_open(self) -> None:
        """Verify callback fires when circuit opens after failures."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        def capture(old: CircuitState, new: CircuitState) -> None:
            transitions.append((old, new))

        breaker = CircuitBreaker(
            failure_threshold=2,
            timeout=0.1,
            name="test_cb",
            on_state_change=capture,
        )

        @breaker
        def failing() -> str:
            raise RuntimeError("boom")

        # Trip the circuit
        for _ in range(2):
            with pytest.raises(RuntimeError):
                failing()

        assert len(transitions) == 1
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)

    def test_callback_on_full_lifecycle(self) -> None:
        """Verify callback fires for CLOSED→OPEN→HALF_OPEN→CLOSED."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        def capture(old: CircuitState, new: CircuitState) -> None:
            transitions.append((old, new))

        breaker = CircuitBreaker(
            failure_threshold=2,
            success_threshold=1,
            timeout=0.05,
            name="lifecycle",
            on_state_change=capture,
        )

        call_should_fail = True

        @breaker
        def service() -> str:
            if call_should_fail:
                raise RuntimeError("down")
            return "ok"

        # Trip the circuit (CLOSED → OPEN)
        for _ in range(2):
            with pytest.raises(RuntimeError):
                service()

        # Wait for timeout (OPEN → HALF_OPEN on next call)
        time.sleep(0.1)

        # Now succeed (HALF_OPEN → CLOSED)
        call_should_fail = False
        result = service()
        assert result == "ok"

        assert len(transitions) == 3
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)
        assert transitions[1] == (CircuitState.OPEN, CircuitState.HALF_OPEN)
        assert transitions[2] == (CircuitState.HALF_OPEN, CircuitState.CLOSED)
