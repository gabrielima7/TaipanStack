"""
Safe subprocess execution with security guards.

Provides secure wrappers around subprocess execution with
command validation, timeout handling, and retry logic.
"""

import os
import shutil
import subprocess  # nosec B404
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from taipanstack.security.guards import (
    _DEFAULT_DENIED_ENV_VARS,
    _SENSITIVE_ENV_VAR_PATTERN,
    SecurityError,
    guard_command_injection,
)


@dataclass(frozen=True)
class SafeCommandResult:
    """Result of a safe command execution.

    Attributes:
        command: The executed command.
        returncode: Exit code of the command.
        stdout: Standard output.
        stderr: Standard error.
        success: Whether the command succeeded (returncode == 0).
        duration_seconds: How long the command took.

    """

    command: list[str]
    returncode: int
    stdout: str = ""
    stderr: str = ""
    duration_seconds: float = 0.0

    @property
    def success(self) -> bool:
        """Check if command succeeded."""
        return self.returncode == 0

    def raise_on_error(self) -> "SafeCommandResult":
        """Raise an exception if command failed.

        Returns:
            Self if successful.

        Raises:
            subprocess.CalledProcessError: If command failed.

        """
        if not self.success:
            raise subprocess.CalledProcessError(
                self.returncode,
                self.command,
                self.stdout,
                self.stderr,
            )
        return self


# Default allowed commands whitelist
DEFAULT_ALLOWED_COMMANDS: frozenset[str] = frozenset(
    {
        # Python/Poetry
        "python",
        "python3",
        "pip",
        "pip3",
        "poetry",
        "pipx",
        # Version control
        "git",
        # Build tools
        "make",
        # Testing
        "pytest",
        "mypy",
        "ruff",
        "bandit",
        "safety",
        "semgrep",
        "pre-commit",
        # System
        "echo",
        "cat",
        "ls",
        "pwd",
        "mkdir",
        "rm",
        "cp",
        "mv",
        "touch",
        "chmod",
        "which",
    }
)


def _validate_and_resolve_command(
    command: Sequence[str],
    allowed_commands: Sequence[str] | None,
) -> list[str]:
    """Validate and resolve a command.

    Args:
        command: Command and arguments as a sequence.
        allowed_commands: Whitelist of allowed commands.

    Returns:
        The validated command as a list.

    Raises:
        SecurityError: If validation fails.

    """
    cmd_list = list(command)

    if not cmd_list:
        raise SecurityError(
            "Empty command is not allowed",
            guard_name="safe_command",
        )

    if allowed_commands is not None:
        whitelist = list(allowed_commands)
    else:
        whitelist = list(DEFAULT_ALLOWED_COMMANDS)

    validated_cmd = guard_command_injection(cmd_list, allowed_commands=whitelist)

    base_command = validated_cmd[0]
    if not shutil.which(base_command):
        raise SecurityError(
            f"Command not found: {base_command}",
            guard_name="safe_command",
            value=base_command,
        )

    return validated_cmd


def _filter_environment(env: dict[str, str] | None) -> dict[str, str]:
    """Filter environment variables for safe execution.

    Args:
        env: Environment variables to filter.

    Returns:
        Filtered environment variables.

    """
    safe_env: dict[str, str] = {}
    env_to_filter = env if env is not None else dict(os.environ)

    for env_key, env_val in env_to_filter.items():
        name_upper = env_key.upper()
        if (
            name_upper not in _DEFAULT_DENIED_ENV_VARS
            and not _SENSITIVE_ENV_VAR_PATTERN.match(name_upper)
        ):
            safe_env[env_key] = str(env_val)

    return safe_env


def _execute_command(
    validated_cmd: list[str],
    cwd: Path | None,
    timeout: float,
    capture_output: bool,
    safe_env: dict[str, str],
) -> SafeCommandResult:
    """Execute the command and handle TimeoutExpired.

    Args:
        validated_cmd: Validated command list.
        cwd: Resolved working directory.
        timeout: Execution timeout.
        capture_output: Capture stdout/stderr.
        safe_env: Filtered environment variables.

    Returns:
        The execution result.

    """
    start_time = time.time()

    try:
        result = subprocess.run(  # nosec B603
            validated_cmd,
            cwd=cwd,
            timeout=timeout,
            capture_output=capture_output,
            text=True,
            encoding="utf-8",
            env=safe_env,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        duration = time.time() - start_time
        stdout_str = ""
        if hasattr(e, "stdout") and e.stdout is not None:  # pragma: no branch
            if isinstance(e.stdout, str):
                stdout_str = e.stdout
            else:  # pragma: no cover
                stdout_str = e.stdout.decode("utf-8", errors="replace")
        return SafeCommandResult(
            command=validated_cmd,
            returncode=-1,
            stdout=stdout_str,
            stderr=f"Command timed out after {timeout}s",
            duration_seconds=duration,
        )

    duration = time.time() - start_time

    return SafeCommandResult(
        command=validated_cmd,
        returncode=result.returncode,
        stdout=result.stdout or "",
        stderr=result.stderr or "",
        duration_seconds=duration,
    )


def run_safe_command(
    command: Sequence[str],
    *,
    cwd: Path | str | None = None,
    timeout: float = 300.0,
    capture_output: bool = True,
    check: bool = False,
    allowed_commands: Sequence[str] | None = None,
    env: dict[str, str] | None = None,
    dry_run: bool = False,
) -> SafeCommandResult:
    """Execute a command safely with security guards.

    This function provides a secure wrapper around subprocess.run
    with command injection protection, timeout handling, and
    optional command whitelisting.

    Args:
        command: Command and arguments as a sequence.
        cwd: Working directory for the command.
        timeout: Maximum execution time in seconds.
        capture_output: Whether to capture stdout/stderr.
        check: Whether to raise on non-zero exit.
        allowed_commands: Whitelist of allowed commands.
        env: Environment variables to set.
        dry_run: If True, don't actually execute the command.

    Returns:
        SafeCommandResult with execution details.

    Raises:
        SecurityError: If command validation fails.
        subprocess.TimeoutExpired: If command times out.
        subprocess.CalledProcessError: If check=True and command fails.

    Example:
        >>> result = run_safe_command(["poetry", "install"])
        >>> if result.success:
        ...     print("Installation complete!")

    """
    validated_cmd = _validate_and_resolve_command(command, allowed_commands)
    safe_env = _filter_environment(env)

    if dry_run:
        return SafeCommandResult(
            command=validated_cmd,
            returncode=0,
            stdout=f"[DRY-RUN] Would execute: {' '.join(validated_cmd)}",
            stderr="",
            duration_seconds=0.0,
        )

    resolved_cwd: Path | None = None
    if cwd is not None:
        resolved_cwd = Path(cwd).resolve()
        if not resolved_cwd.exists():
            raise SecurityError(
                f"Working directory does not exist: {cwd}",
                guard_name="safe_command",
            )

    safe_result = _execute_command(
        validated_cmd,
        resolved_cwd,
        timeout,
        capture_output,
        safe_env,
    )

    if check:
        safe_result.raise_on_error()

    return safe_result
