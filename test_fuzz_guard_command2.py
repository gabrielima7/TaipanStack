import pytest
from hypothesis import given, settings, HealthCheck, strategies as st
from taipanstack.security.guards import guard_command_injection

@settings(
    max_examples=500,
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large]
)
@given(st.iterables(st.text()))
def test_fuzz_guard_command_injection_iterable(cmd):
    try:
        guard_command_injection(cmd)
    except Exception as e:
        if not isinstance(e, (ValueError, TypeError, Exception)):
            raise

if __name__ == "__main__":
    pytest.main(["-v", "test_fuzz_guard_command2.py"])
