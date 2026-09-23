"""Chaos tests for resilience timeout decorator."""

import pytest

from taipanstack.core.result import Ok
from taipanstack.resilience.resilience import timeout


def test_resilience_chaos_timeout_corrupt_float_expected() -> None:
    """Verify sync timeout returns Err(ValueError) when receiving corrupted float."""

    class CorruptFloat(float):
        def __ge__(self, other: object) -> bool:
            raise RuntimeError("Chaos __ge__")

        def __add__(self, other: object) -> float:
            raise RuntimeError("Chaos __add__")

        def __mul__(self, other: object) -> float:
            raise RuntimeError("Chaos __mul__")

        def __lt__(self, other: object) -> bool:
            raise RuntimeError("Chaos __lt__")

    @timeout(CorruptFloat(1.0))
    def my_func() -> Ok[int]:
        return Ok(1)

    result = my_func()
    assert result.is_err()
    assert isinstance(result.err_value, ValueError)


def test_timeout_bool_chaos() -> None:
    """Verify timeout rejects boolean inputs instead of treating them as integers."""

    @timeout(True)  # type: ignore[arg-type]
    def func_true() -> Ok[int]:
        return Ok(1)

    res_true = func_true()
    assert res_true.is_err()
    assert isinstance(res_true.err_value, ValueError)


@pytest.mark.asyncio
async def test_timeout_chaos_type_mutation_async() -> None:
    """Verify async timeout returns Err(ValueError) when receiving corrupted float."""

    class EvilFloat(float):
        def __ge__(self, other: object) -> bool:
            raise RuntimeError("Chaos __ge__")

        def __add__(self, other: object) -> float:
            raise RuntimeError("Chaos __add__")

        def __mul__(self, other: object) -> float:
            raise RuntimeError("Chaos __mul__")

        def __lt__(self, other: object) -> bool:
            raise RuntimeError("Chaos __lt__")

    @timeout(EvilFloat(1.0))
    async def my_func() -> Ok[int]:
        return Ok(1)

    result = await my_func()
    assert result.is_err()
    assert isinstance(result.err_value, ValueError)
