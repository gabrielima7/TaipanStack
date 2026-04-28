import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import SecurityError, guard_command_injection


@settings(
    max_examples=500,
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large]
)
@given(st.lists(st.text()))
def test_fuzz_guard_command_generator(cmd_list):
    def gen():
        yield from cmd_list

    try:
        guard_command_injection(gen())
    except SecurityError:
        pass  # Expected for invalid commands or empty commands
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError)):
            pytest.fail(f"Unexpected exception: {e}")

def test_guard_command_empty_generator_expected():
    def empty_gen():
        yield from ()

    with pytest.raises(SecurityError, match="Empty command is not allowed"):
        guard_command_injection(empty_gen())
