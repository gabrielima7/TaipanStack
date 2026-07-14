from typing import cast

import pytest

from taipanstack.core.result import Ok, Result
from taipanstack.resilience.resilience import fallback


def test_chaos_fallback_exceptions_tuple_mutation_execution_success() -> None:
    """Simulate type corruption where exceptions parameter is mutated.
    Instead of passing the exception or crashing, it should safely raise it."""

    @fallback("fallback", exceptions=cast(tuple, "string_mutation"))
    def sync_dummy() -> Result[str, Exception]:
        raise ValueError("Original exception")

    with pytest.raises(ValueError, match="Original exception"):
        sync_dummy()


@pytest.mark.asyncio
async def test_chaos_fallback_exceptions_tuple_mutation_async_execution_success() -> None:
    """Simulate type corruption where exceptions parameter is mutated in async."""

    @fallback("fallback", exceptions=cast(tuple, "string_mutation"))
    async def async_dummy() -> Result[str, Exception]:
        raise ValueError("Original exception async")

    with pytest.raises(ValueError, match="Original exception async"):
        await async_dummy()


def test_chaos_fallback_exceptions_tuple_mutation_sync_result_execution_success() -> None:
    """Simulate type corruption where exceptions parameter is mutated, but function returns Ok."""

    @fallback("fallback", exceptions=cast(tuple, "string_mutation"))
    def sync_dummy() -> Result[str, Exception]:
        return Ok("success")

    assert sync_dummy() == Ok("success")


@pytest.mark.asyncio
async def test_chaos_fallback_exceptions_tuple_mutation_async_result_execution_success() -> None:
    """Simulate type corruption where exceptions parameter is mutated, but async function returns Ok."""

    @fallback("fallback", exceptions=cast(tuple, "string_mutation"))
    async def async_dummy() -> Result[str, Exception]:
        return Ok("success")

    assert await async_dummy() == Ok("success")
