import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import guard_env_variable
from taipanstack.security.types import SecurityError
from taipanstack.security.validators import MAX_ENV_VAR_LENGTH


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    max_examples=10,
    deadline=None,
)
@given(st.text(min_size=MAX_ENV_VAR_LENGTH + 1, max_size=8192))
def test_fuzz_guard_env_variable_massive_strings_dos_returns_err_execution_success(
    name: str,
) -> None:
    """Fuzz guard_env_variable with massive strings to ensure DoS protection limits are active."""
    with pytest.raises(SecurityError):
        guard_env_variable(name)
