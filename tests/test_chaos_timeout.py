import pytest

from taipanstack.core.result import Result
from taipanstack.resilience.resilience import timeout


def test_chaos_timeout_system_exit() -> None:
    @timeout(1.0)
    def worker_func() -> Result[str, Exception]:
        raise SystemExit("Simulated catastrophic failure")

    with pytest.raises(SystemExit, match="Simulated catastrophic failure"):
        worker_func()

class CustomBaseException(BaseException):
    pass

def test_chaos_timeout_base_exception() -> None:
    @timeout(1.0)
    def worker_func() -> Result[str, Exception]:
        raise CustomBaseException("Simulated base exception failure")

    with pytest.raises(CustomBaseException, match="Simulated base exception failure"):
        worker_func()
