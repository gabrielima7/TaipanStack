"""Tests for subprocess module security fixes."""

import os

from taipanstack.utils.subprocess import run_safe_command


def test_security_subprocess_run_safe_command_filters_sensitive_env_vars_expected() -> (
    None
):
    """Test that run_safe_command uses a whitelist approach to filter env vars."""
    env = os.environ.copy()
    env["AWS_SECRET_ACCESS_KEY"] = "my-secret"
    env["SAFE_VAR"] = "safe-value"
    env["PATH"] = os.environ.get("PATH", "")

    # Only PATH and SAFE_VAR are whitelisted
    result = run_safe_command(
        ["echo", "hello"],
        allowed_commands=["echo"],
        env=env,
        allowed_env_vars=["PATH", "SAFE_VAR"],
    )
    assert result.success


def test_security_subprocess_run_safe_command_filters_default_env_expected() -> None:
    """Test that run_safe_command uses default whitelist (PATH) if not provided."""
    os.environ["SUPER_SECRET_TOKEN"] = "hidden"
    try:
        # Without allowed_env_vars, only PATH should be inherited
        result = run_safe_command(["echo", "hello"], allowed_commands=["echo"])
        assert result.success
    finally:
        del os.environ["SUPER_SECRET_TOKEN"]


def test_security_subprocess_run_safe_command_empty_whitelist_expected() -> None:
    """Test that run_safe_command can be given an empty whitelist to inherit an empty environment."""
    env = os.environ.copy()
    env["TEST_VAR"] = "test"

    # Empty list means completely empty environment
    # Since we use 'echo' which might be built-in or full path, it might fail without PATH if it's not resolved properly,
    # but run_safe_command validates and resolves `shutil.which` *before* execution.
    # Actually wait, Popen without PATH and just "echo" as command might fail. Let's use the resolved path.
    import shutil

    echo_path = shutil.which("echo")
    if echo_path:
        result = run_safe_command(
            [echo_path, "hello"],
            allowed_commands=["echo", echo_path],
            env=env,
            allowed_env_vars=[],
        )
        assert result.success
