import pytest
from taipanstack.resilience.resilience import timeout
from taipanstack.core.result import Result


def test_chaos_timeout_uncatchable_exception_in_thread():
    @timeout(5.0)
    def chaotic_function() -> Result[str, Exception]:
        raise SystemExit("SystemExit chaos injected")

    with pytest.raises(SystemExit, match="SystemExit chaos injected"):
        chaotic_function()
