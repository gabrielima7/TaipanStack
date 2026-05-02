import contextlib

from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_env_variable,
)


@given(st.lists(st.text(), min_size=1))
def test_guard_command_injection_fuzz(cmd):
    with contextlib.suppress(SecurityError):
        guard_command_injection(cmd)


@given(st.text())
def test_guard_env_variable_fuzz(env):
    with contextlib.suppress(SecurityError):
        guard_env_variable(env)


def test_guard_command_injection_null_byte():
    import pytest

    with pytest.raises(SecurityError, match="null byte"):
        guard_command_injection(["\x00"])


def test_guard_env_variable_null_byte():
    import pytest

    with pytest.raises(SecurityError, match="null byte"):
        guard_env_variable("\x00")
