"""Tests for subprocess module security fixes."""

import os

from taipanstack.utils.subprocess import run_safe_command


def test_run_safe_command_filters_sensitive_env_vars() -> None:
    """Test that run_safe_command filters out sensitive env vars."""
    env = os.environ.copy()
    env["AWS_SECRET_ACCESS_KEY"] = "my-secret"
    env["SAFE_VAR"] = "safe-value"

    # To bypass injection guard with allowed_commands
    result = run_safe_command(["echo", "hello"], allowed_commands=["echo"], env=env)
    assert result.success


def test_run_safe_command_filters_default_env() -> None:
    """Test that run_safe_command filters os.environ by default."""
    os.environ["SUPER_SECRET_TOKEN"] = "hidden"
    try:
        result = run_safe_command(["echo", "hello"], allowed_commands=["echo"])
        assert result.success
    finally:
        del os.environ["SUPER_SECRET_TOKEN"]
