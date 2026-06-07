from typing import cast

import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.resilience import timeout


def test_chaos_resilience_timeout_type_mutation_standard_expected() -> None:
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
