import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.bulkhead import Bulkhead


def test_chaos_adaptive_limits_retry_overflow():
    ar = AdaptiveRetry(min_delay=0.1, max_delay=30.0)
    # Attempt 2000 used to overflow 2.0 ** 1999
    delay = ar.get_delay(2000)
    assert delay == 30.0


@given(
    max_concurrent=st.one_of(st.integers(max_value=0), st.floats(), st.text(), st.booleans()),
    max_queue=st.one_of(st.integers(max_value=-1), st.floats(), st.text(), st.booleans()),
)
def test_chaos_adaptive_limits_bulkhead_invalid_params(max_concurrent, max_queue):
    with pytest.raises((ValueError, TypeError)):
        Bulkhead(max_concurrent=max_concurrent)

    with pytest.raises((ValueError, TypeError)):
        Bulkhead(max_queue=max_queue)
