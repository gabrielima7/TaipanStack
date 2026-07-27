import pytest

from taipanstack.resilience.resilience import fallback


def test_resilience_resilience_unreachable_resilience_fallback_unreachable_sync_expected():
    """Test unreachable condition in sync fallback wrapper."""

    @fallback("fallback_val", exceptions=(ValueError,))
    def dummy():
        return "Not a Result Type"  # Type is invalid, breaking contract

    result = dummy()
    assert result.is_err()
    assert str(result.unwrap_err()) == "Unreachable"


@pytest.mark.asyncio
async def test_resilience_resilience_unreachable_resilience_fallback_unreachable_async():
    """Test unreachable condition in async fallback wrapper."""

    @fallback("fallback_val", exceptions=(ValueError,))
    async def dummy():
        return "Not a Result Type"  # Type is invalid, breaking contract

    result = await dummy()
    assert result.is_err()
    assert str(result.unwrap_err()) == "Unreachable"
