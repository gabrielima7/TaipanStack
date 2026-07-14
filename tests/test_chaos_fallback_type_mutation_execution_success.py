import pytest

from taipanstack.core.result import Result
from taipanstack.resilience.resilience import fallback


def test_chaos_fallback_chaos_type_mutation_sync_execution_success():
    """Verify fallback exception tuple mutation safely defaults to re-raising original error."""
    # We mutate it to an integer or string

    @fallback("fallback", exceptions=123)  # type: ignore
    def broken() -> Result[str, Exception]:
        raise ValueError("inner failure")

    with pytest.raises(ValueError, match="inner failure"):
        broken()


@pytest.mark.asyncio
async def test_chaos_fallback_chaos_type_mutation_async_execution_success():
    """Verify fallback exception tuple mutation safely defaults to re-raising original error in async."""

    @fallback("fallback", exceptions=123)  # type: ignore
    async def async_broken() -> Result[str, Exception]:
        raise ValueError("inner failure async")

    with pytest.raises(ValueError, match="inner failure async"):
        await async_broken()
