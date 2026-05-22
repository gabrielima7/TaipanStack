import pytest
from typing import cast
from taipanstack.resilience.resilience import timeout
from taipanstack.core.result import Result, Ok, Err

def test_chaos_resilience_timeout_type_mutation() -> None:
    """Simulate a severe production failure where timeout 'seconds' is corrupted to a string."""
    @timeout(cast(float, "1.0"))
    def dummy() -> Result[str, Exception]:
        return Ok("success")

    result = dummy()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)


@pytest.mark.asyncio
async def test_chaos_resilience_timeout_type_mutation_async() -> None:
    """Simulate a severe production failure where timeout 'seconds' is corrupted to a string."""
    @timeout(cast(float, "1.0"))
    async def dummy() -> Result[str, Exception]:
        return Ok("success")

    result = await dummy()
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)
