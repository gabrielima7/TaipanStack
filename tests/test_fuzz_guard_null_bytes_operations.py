from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_env_variable,
)


@given(st.lists(st.text(), min_size=1))
def test_fuzz_guard_null_bytes_guard_command_injection_fuzz_returns_ok_or_raises_error(cmd):
    try:
        result = guard_command_injection(cmd)
        assert isinstance(result, list)
    except Exception as e:
        assert isinstance(e, (SecurityError, ValueError, TypeError))


@given(st.text())
def test_fuzz_guard_null_bytes_guard_env_variable_fuzz_returns_ok_or_raises_error(env):
    try:
        result = guard_env_variable(env)
        assert isinstance(result, str)
    except Exception as e:
        assert isinstance(e, (SecurityError, ValueError, TypeError))


def test_fuzz_guard_null_bytes_guard_command_injection_null_byte_raises_error():
    import pytest

    with pytest.raises(SecurityError, match="null byte"):
        guard_command_injection(["\x00"])


def test_fuzz_guard_null_bytes_guard_env_variable_null_byte_raises_error():
    import pytest

    with pytest.raises(SecurityError, match="null byte"):
        guard_env_variable("\x00")
