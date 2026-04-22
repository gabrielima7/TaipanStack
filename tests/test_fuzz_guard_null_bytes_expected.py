import contextlib

from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_env_variable,
)


@given(st.lists(st.text(), min_size=1))
def test_guard_command_injection_fuzz_expected(cmd):
    with contextlib.suppress(SecurityError):
        guard_command_injection(cmd)


@given(st.text())
def test_guard_env_variable_fuzz_expected(env):
    with contextlib.suppress(SecurityError):
        guard_env_variable(env)
