import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import _check_ip_safety


@settings(deadline=None)
@given(st.text())
def test_fuzz_check_ip_safety(hostname):
    try:
        _check_ip_safety(hostname)
    except TypeError:
        pass
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")
