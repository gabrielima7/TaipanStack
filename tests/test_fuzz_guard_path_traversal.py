import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from taipanstack.security.guards import guard_path_traversal, SecurityError

@settings(max_examples=5000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(st.text())
def test_fuzz_guard_path_traversal(path):
    try:
        guard_path_traversal(path)
    except TypeError:
        pass
    except SecurityError:
        pass
    except Exception as e:
        pytest.fail(f"Unexpected exception for input {repr(path)}: {e}")
