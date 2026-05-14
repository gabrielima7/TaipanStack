import threading

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.resilience import timeout


def test_timeout_chaos_type_mutation():
    """Test what happens if the timeout value is not a finite number."""
    import math

    @timeout(math.nan)
    def flaky_func() -> Result[str, Exception]:
        return Ok("Success")

    result = flaky_func()
    assert isinstance(result, Err), "NaN timeout should fail safely"
    assert isinstance(
        result.unwrap_err(), ValueError
    ), "Should return ValueError for invalid timeout"


def test_timeout_chaos_thread_exhaustion():
    """Simulate thread exhaustion for sync timeout."""

    # We will mock threading.Thread to raise RuntimeError
    original_thread = threading.Thread

    class MockThread:
        def __init__(self, *args, **kwargs):
            pass

        def start(self):
            raise RuntimeError("can't start new thread")

    threading.Thread = MockThread  # type: ignore

    try:

        @timeout(1.0)
        def flaky_func() -> Result[str, Exception]:
            return Ok("Success")

        result = flaky_func()
        assert isinstance(result, Err), "Thread exhaustion should be caught"
        assert isinstance(
            result.unwrap_err(), RuntimeError
        ), "Should return RuntimeError on thread failure"
    finally:
        threading.Thread = original_thread
