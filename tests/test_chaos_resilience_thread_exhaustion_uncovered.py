from unittest import mock

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout


def test_chaos_timeout_thread_exhaustion_init():
    @timeout(1.0)
    def my_func():
        return Ok(42)

    with mock.patch("threading.Thread") as mock_thread:
        mock_thread.side_effect = RuntimeError("can't start new thread")
        res = my_func()
        assert isinstance(res, Err)
        assert "Thread exhaustion: can't start new thread" in str(res.unwrap_err())
