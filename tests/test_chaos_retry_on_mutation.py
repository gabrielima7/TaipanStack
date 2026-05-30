import asyncio

import pytest

from taipanstack.resilience.retry import retry


def test_chaos_retry_on_mutation():
    corrupted_on = "NotAnException"

    @retry(max_attempts=2, on=corrupted_on) # type: ignore
    def faulty_func():
        raise ValueError("Fail")

    with pytest.raises(ValueError, match="Fail"):
        faulty_func()

def test_chaos_retry_async_on_mutation():
    corrupted_on = "NotAnException"

    @retry(max_attempts=2, on=corrupted_on) # type: ignore
    async def faulty_func_async():
        raise ValueError("Fail async")

    with pytest.raises(ValueError, match="Fail async"):
        asyncio.run(faulty_func_async())

def test_chaos_retry_not_instance_exception() -> None:
    @retry(max_attempts=2, on=(ValueError,))
    def faulty_func_not_isinstance():
        raise KeyError("Key")

    with pytest.raises(KeyError, match="Key"):
        faulty_func_not_isinstance()

def test_chaos_retry_async_not_instance_exception() -> None:
    @retry(max_attempts=2, on=(ValueError,))
    async def faulty_func_async_not_isinstance():
        raise KeyError("Key async")

    with pytest.raises(KeyError, match="Key async"):
        asyncio.run(faulty_func_async_not_isinstance())

def test_chaos_retry_err_val_type_error() -> None:
    from taipanstack.core.result import Err

    corrupted_on = "NotAnException"

    @retry(max_attempts=2, on=corrupted_on) # type: ignore
    def faulty_func_err():
        return Err(ValueError("err"))

    # We should get Err because it can't check isinstance with corrupted on and just returns it
    res = faulty_func_err()
    assert res.is_err()

def test_chaos_retry_async_err_val_type_error() -> None:
    from taipanstack.core.result import Err

    corrupted_on = "NotAnException"

    @retry(max_attempts=2, on=corrupted_on) # type: ignore
    async def faulty_func_async_err():
        return Err(ValueError("err async"))

    # We should get Err
    res = asyncio.run(faulty_func_async_err())
    assert res.is_err()
