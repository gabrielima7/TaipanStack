import pytest

from taipanstack.resilience.resilience import timeout


def test_sync_timeout_base_exception_chaos() -> None:
    """Chaos test: simulate uncatchable exception (BaseException/SystemExit) inside the worker thread.

    If the worker thread crashes with an exception inheriting from BaseException rather than Exception,
    the original timeout logic would let the thread die silently without populating the exception list.
    Then, the main thread would encounter an IndexError when attempting to access result[0].
    This test verifies that the uncatchable exception is properly caught and propagated to the main thread.
    """

    @timeout(1.0)
    def suicidal_task() -> None:
        raise SystemExit(0)

    # It should correctly propagate the SystemExit, not raise an IndexError
    with pytest.raises(SystemExit):
        suicidal_task()
