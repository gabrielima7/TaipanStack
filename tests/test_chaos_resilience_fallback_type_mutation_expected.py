"""Chaos tests for resilience fallback type mutation."""

import pytest

from taipanstack.core.result import Ok
from taipanstack.resilience.resilience import fallback


def test_chaos_resilience_fallback_type_mutation_expected() -> None:
    """Simulate a severe production failure where fallback 'exceptions' is corrupted to a string."""

    @fallback("fallback_val", exceptions="string_mutation")  # type: ignore
    def dummy():
        raise ValueError("Original failure")

    with pytest.raises(ValueError, match="Original failure"):
        dummy()


@pytest.mark.asyncio
async def test_chaos_resilience_fallback_type_mutation_async_expected() -> (
    None
):
    """Simulate a severe production failure where fallback 'exceptions' is corrupted to a string."""

    @fallback("fallback_val", exceptions="string_mutation")  # type: ignore
    async def dummy():
        raise ValueError("Original failure")

    with pytest.raises(ValueError, match="Original failure"):
        await dummy()


def test_chaos_resilience_fallback_type_mutation_success_expected() -> None:
    """Test standard success behavior when exceptions type is invalid."""

    @fallback("fallback_val", exceptions="string_mutation")  # type: ignore
    def dummy():
        return Ok("success")

    assert dummy().unwrap() == "success"


@pytest.mark.asyncio
async def test_chaos_resilience_fallback_type_mutation_async_success_expected() -> (
    None
):
    """Test standard success behavior for async when exceptions type is invalid."""

    @fallback("fallback_val", exceptions="string_mutation")  # type: ignore
    async def dummy():
        return Ok("success")

    result = await dummy()
    assert result.unwrap() == "success"


def test_chaos_resilience_fallback_type_mutation_not_isinstance_expected() -> (
    None
):
    """Coverage: valid type but not matching."""

    @fallback("fallback_val", exceptions=(ValueError,))
    def dummy():
        raise TypeError("Different error")

    with pytest.raises(TypeError, match="Different error"):
        dummy()


@pytest.mark.asyncio
async def test_chaos_resilience_fallback_type_mutation_async_not_isinstance_expected() -> (
    None
):
    """Coverage: valid type but not matching."""

    @fallback("fallback_val", exceptions=(ValueError,))
    async def dummy():
        raise TypeError("Different error")

    with pytest.raises(TypeError, match="Different error"):
        await dummy()
