from unittest import mock

from taipanstack.core.result import Ok
from taipanstack.resilience.resilience import timeout


@timeout(1.0)
def dummy_func() -> Ok[str]:
    return Ok("success")


def test_chaos_resilience_thread_dies_abruptly() -> None:
    # Simulate a scenario where the thread dies abruptly before appending to result or exception
    # by mocking thread.is_alive() to return False when _process_sync_timeout_result checks it.

    with (
        mock.patch("threading.Thread.is_alive", return_value=False),
        mock.patch("threading.Thread.join", return_value=None),
        mock.patch("threading.Thread.start", return_value=None),
    ):
        res = dummy_func()
        assert res.is_err()
        assert "Thread died abruptly" in str(res.unwrap_err())
