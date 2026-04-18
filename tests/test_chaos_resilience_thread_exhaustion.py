from unittest import mock

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.resilience import timeout


def test_timeout_thread_exhaustion():
    @timeout(1.0)
    def my_func():
        return Ok("done")

    with mock.patch(
        "threading.Thread.start", side_effect=RuntimeError("can't start new thread")
    ):
        result = my_func()
        assert isinstance(result, Err)
        assert "Thread exhaustion: can't start new thread" in str(result.unwrap_err())


if __name__ == "__main__":
    test_timeout_thread_exhaustion()
