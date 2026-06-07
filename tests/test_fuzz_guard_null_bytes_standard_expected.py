import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.guards import (
    SecurityError,
    _validate_env_var_name,
    guard_command_injection,
    guard_env_variable,
)


@given(st.lists(st.text(), min_size=1))
def test_fuzz_guard_null_bytes_command_injection_ok_or_raises_standard_expected(cmd):
    try:
        result = guard_command_injection(cmd)
        assert isinstance(result, list)
    except Exception as e:
        assert isinstance(e, (SecurityError, ValueError, TypeError))


@given(st.text())
def test_fuzz_guard_null_bytes_env_variable_ok_or_raises_standard_expected(env):
    try:
        result = guard_env_variable(env)
        assert isinstance(result, str)
    except Exception as e:
        assert isinstance(e, (SecurityError, ValueError, TypeError))


def test_fuzz_guard_null_bytes_command_injection_raises_error_standard_expected():
    with pytest.raises(SecurityError, match="null byte"):
        guard_command_injection(["\x00"])


def test_fuzz_guard_null_bytes_env_variable_raises_error_standard_expected():
    with pytest.raises(SecurityError, match="null byte"):
        guard_env_variable("\x00")


def test_fuzz_guard_null_bytes_env_variable_empty_string_raises_error_standard_expected():
    with pytest.raises(SecurityError, match="empty or whitespace"):
        _validate_env_var_name("   ")


def test_fuzz_guard_null_bytes_env_variable_empty_string2_raises_error_standard_expected():
    with pytest.raises(SecurityError, match="empty or whitespace"):
        _validate_env_var_name("")


def test_fuzz_guard_null_bytes_env_variable_name_raises_error_standard_expected():
    with pytest.raises(SecurityError, match="null byte"):
        _validate_env_var_name("\x00name")
