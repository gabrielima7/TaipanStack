from unittest.mock import patch

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout


def test_chaos_timeout_resource_exhaustion_thread_oserror_returns_err_execution_success():
    @timeout(1.0)
    def dummy_task():
        return Ok("success")

    with patch(
        "threading.Thread.start",
        side_effect=OSError("Resource temporarily unavailable"),
    ):
        result = dummy_task()
        assert isinstance(result, Err)
        assert "Resource exhaustion" in str(result.unwrap_err())


def test_chaos_timeout_resource_exhaustion_thread_memoryerror_returns_err_execution_success():
    @timeout(1.0)
    def dummy_task():
        return Ok("success")

    with patch("threading.Thread.start", side_effect=MemoryError("Out of memory")):
        result = dummy_task()
        assert isinstance(result, Err)
        assert "Memory exhaustion" in str(result.unwrap_err())
