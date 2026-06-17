"""Tests for safe subprocess execution utilities."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from taipanstack.security.guards import SecurityError
from taipanstack.utils.subprocess import (
    DEFAULT_ALLOWED_COMMANDS,
    SafeCommandResult,
    _execute_command,
    run_safe_command,
)


class TestSafeCommandResult:
    """Tests for SafeCommandResult dataclass."""

    def test_utils_subprocess_success_true_when_returncode_zero_standard_expected(
        self,
    ) -> None:
        """Test success property returns True for returncode 0."""
        result = SafeCommandResult(
            command=["echo", "hello"],
            returncode=0,
            stdout="hello\n",
            stderr="",
        )
        assert result.success is True

    def test_utils_subprocess_success_false_when_returncode_nonzero_standard_expected(
        self,
    ) -> None:
        """Test success property returns False for non-zero returncode."""
        result = SafeCommandResult(
            command=["false"],
            returncode=1,
            stdout="",
            stderr="error",
        )
        assert result.success is False

    def test_utils_subprocess_raise_on_error_success_standard_expected(self) -> None:
        """Test raise_on_error returns self on success."""
        result = SafeCommandResult(
            command=["echo", "test"],
            returncode=0,
            stdout="test\n",
        )
        assert result.raise_on_error() is result

    def test_utils_subprocess_raise_on_error_failure_standard_expected(self) -> None:
        """Test raise_on_error raises CalledProcessError on failure."""
        result = SafeCommandResult(
            command=["bad", "command"],
            returncode=1,
            stdout="",
            stderr="error message",
        )
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            result.raise_on_error()
        assert exc_info.value.returncode == 1
        assert exc_info.value.cmd == ["bad", "command"]

    def test_utils_subprocess_duration_seconds_default_standard_expected(self) -> None:
        """Test duration_seconds has default value."""
        result = SafeCommandResult(command=["test"], returncode=0)
        assert result.duration_seconds == 0.0


class TestDefaultAllowedCommands:
    """Tests for DEFAULT_ALLOWED_COMMANDS."""

    def test_utils_subprocess_contains_essential_commands_standard_expected(
        self,
    ) -> None:
        """Test that essential commands are in the whitelist."""
        essential = ["python", "poetry", "git", "pytest", "mypy", "ruff"]
        for cmd in essential:
            assert cmd in DEFAULT_ALLOWED_COMMANDS

    def test_utils_subprocess_is_frozenset_standard_expected(self) -> None:
        """Test that it's immutable."""
        assert isinstance(DEFAULT_ALLOWED_COMMANDS, frozenset)


class TestRunSafeCommand:
    """Tests for run_safe_command function."""

    def test_utils_subprocess_run_echo_command_standard_expected(self) -> None:
        """Test running a simple echo command."""
        result = run_safe_command(["echo", "hello"])
        assert result.success is True
        assert "hello" in result.stdout
        assert result.returncode == 0

    def test_utils_subprocess_dry_run_mode_standard_expected(self) -> None:
        """Test dry-run mode doesn't execute command."""
        result = run_safe_command(["rm", "-rf", "/"], dry_run=True)
        assert result.success is True
        assert "[DRY-RUN]" in result.stdout
        assert result.returncode == 0

    def test_utils_subprocess_command_not_in_whitelist_standard_expected(self) -> None:
        """Test that commands not in whitelist are rejected."""
        with pytest.raises(SecurityError, match="Command not in allowed list"):
            run_safe_command(
                ["dangerous_command"],
                allowed_commands=["safe_command"],
            )

    def test_utils_subprocess_empty_command_rejected_standard_expected(self) -> None:
        """Test that empty command raises SecurityError."""
        with pytest.raises(SecurityError, match="Empty command"):
            run_safe_command([])

    def test_utils_subprocess_command_injection_blocked_standard_expected(self) -> None:
        """Test that shell metacharacters are blocked."""
        with pytest.raises(SecurityError, match="Dangerous"):
            run_safe_command(["echo", "hello; rm -rf /"])

    def test_utils_subprocess_command_not_found_standard_expected(self) -> None:
        """Test that non-existent command raises SecurityError."""
        with pytest.raises(SecurityError, match="Command not found"):
            run_safe_command(
                ["nonexistent_command_xyz"],
                allowed_commands=["nonexistent_command_xyz"],
            )

    def test_utils_subprocess_timeout_handling_standard_expected(self) -> None:
        """Test command timeout is handled."""
        # Use sleep command which is safer than Python -c with semicolons
        result = run_safe_command(
            ["sleep", "5"],
            timeout=0.1,
            allowed_commands=["sleep"],
        )
        assert result.success is False
        assert result.returncode == -1
        assert "timed out" in result.stderr

    def test_utils_subprocess_working_directory_standard_expected(
        self, tmp_path: Path
    ) -> None:
        """Test that working directory is respected."""
        # Create a file in tmp_path to verify we can access it
        test_file = tmp_path / "test_cwd.txt"
        test_file.write_text("test")

        # Use echo which works on both Windows and Linux
        result = run_safe_command(
            ["echo", "hello"],
            cwd=tmp_path,
        )
        assert result.success is True

    def test_utils_subprocess_invalid_working_directory_standard_expected(self) -> None:
        """Test that non-existent working directory raises error."""
        with pytest.raises(SecurityError, match="Working directory does not exist"):
            run_safe_command(["echo", "test"], cwd="/nonexistent/path/xyz")

    def test_utils_subprocess_custom_allowed_commands_standard_expected(self) -> None:
        """Test custom allowed commands list."""
        result = run_safe_command(
            ["echo", "custom"],
            allowed_commands=["echo"],
        )
        assert result.success is True

    def test_utils_subprocess_duration_is_tracked_standard_expected(self) -> None:
        """Test that command duration is tracked."""
        result = run_safe_command(["echo", "test"])
        assert result.duration_seconds >= 0

    def test_utils_subprocess_timeout_negative_value_standard_expected(self) -> None:
        """Test timeout with negative seconds."""
        with pytest.raises(
            ValueError, match="timeout must be a finite non-negative number"
        ):
            run_safe_command(["echo", "hello"], timeout=-1.0)

    def test_utils_subprocess_timeout_nan_value_standard_expected(self) -> None:
        """Test timeout with NaN seconds."""
        with pytest.raises(
            ValueError, match="timeout must be a finite non-negative number"
        ):
            run_safe_command(["echo", "hello"], timeout=float("nan"))

    def test_utils_subprocess_timeout_inf_value_standard_expected(self) -> None:
        """Test timeout with Infinity seconds."""
        with pytest.raises(
            ValueError, match="timeout must be a finite non-negative number"
        ):
            run_safe_command(["echo", "hello"], timeout=float("inf"))


def test_utils_subprocess_execute_command_timeout_with_bytes_stdout_standard_expected() -> (
    None
):
    """Test _execute_command timeout handling when stdout is bytes."""
    with patch("subprocess.run") as mock_run:
        err = subprocess.TimeoutExpired(["sleep", "10"], 1.0)
        err.stdout = b"some bytes output"
        mock_run.side_effect = err

        result = _execute_command(["sleep", "10"], None, 1.0, True, {})

        assert result.returncode == -1
        assert result.stdout == "some bytes output"


def test_utils_subprocess_execute_command_timeout_without_stdout_standard_expected() -> (
    None
):
    """Test _execute_command timeout handling when stdout is None."""
    with patch("subprocess.run") as mock_run:
        err = subprocess.TimeoutExpired(["sleep", "10"], 1.0)
        err.stdout = None
        mock_run.side_effect = err

        result = _execute_command(["sleep", "10"], None, 1.0, True, {})

        assert result.returncode == -1
        assert result.stdout == ""


def test_utils_subprocess_execute_command_timeout_with_str_stdout_standard_expected() -> (
    None
):
    """Test _execute_command timeout handling when stdout is str."""
    with patch("subprocess.run") as mock_run:
        err = subprocess.TimeoutExpired(["sleep", "10"], 1.0)
        err.stdout = "some text output"
        mock_run.side_effect = err

        result = _execute_command(["sleep", "10"], None, 1.0, True, {})

        assert result.returncode == -1
        assert result.stdout == "some text output"
