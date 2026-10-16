import pytest

from taipanstack.core.result import Result
from taipanstack.resilience.resilience import fallback


def test_resilience_fallback_type_error_sync() -> None:
    """Test that passing an invalid exceptions type triggers the TypeError catch block."""

    # Passing an invalid type (string) to exceptions to trigger TypeError in isinstance
    @fallback("fallback_val", exceptions="NotAnExceptionType")  # type: ignore[arg-type]
    def dummy_func() -> Result[str, Exception]:
        raise ValueError("Failed")

    with pytest.raises(ValueError):
        dummy_func()

@pytest.mark.asyncio
async def test_resilience_fallback_type_error_async() -> None:
    """Test that passing an invalid exceptions type triggers the TypeError catch block in async context."""

    @fallback("fallback_val", exceptions="NotAnExceptionType")  # type: ignore[arg-type]
    async def dummy_func() -> Result[str, Exception]:
        raise ValueError("Failed")

    with pytest.raises(ValueError):
        await dummy_func()
