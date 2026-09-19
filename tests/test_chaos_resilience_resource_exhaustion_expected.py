from unittest import mock

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout


def test_chaos_resilience_resource_exhaustion_timeout_expected():
    @timeout(1.0)
    def my_func():
        return Ok("done")

    with mock.patch(
        "threading.Thread.start", side_effect=OSError("Too many open files")
    ):
        result = my_func()
        assert isinstance(result, Err)
        assert "Resource exhaustion: Too many open files" in str(result.unwrap_err())


def test_chaos_resilience_resource_exhaustion_chaos_resilience_memory_exhaustion_timeout_expected():
    @timeout(1.0)
    def my_func():
        return Ok("done")

    with mock.patch("threading.Thread.start", side_effect=MemoryError("Out of memory")):
        result = my_func()
        assert isinstance(result, Err)
        assert "Memory exhaustion: Out of memory" in str(result.unwrap_err())
