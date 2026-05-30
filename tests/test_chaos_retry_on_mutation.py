import asyncio

import pytest

from taipanstack.resilience.retry import retry


def test_chaos_retry_on_mutation():
    corrupted_on = "NotAnException"

    with pytest.raises(TypeError, match="'on' parameter must be an exception class or a tuple of exception classes"):
        @retry(max_attempts=2, on=corrupted_on)  # type: ignore
        def faulty_func():
            pass


def test_chaos_retry_async_on_mutation():
    corrupted_on = "NotAnException"

    with pytest.raises(TypeError, match="'on' parameter must be an exception class or a tuple of exception classes"):
        @retry(max_attempts=2, on=corrupted_on)  # type: ignore
        async def faulty_func_async():
            pass


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
    corrupted_on = "NotAnException"

    with pytest.raises(TypeError, match="'on' parameter must be an exception class or a tuple of exception classes"):
        @retry(max_attempts=2, on=corrupted_on)  # type: ignore
        def faulty_func_err():
            pass


def test_chaos_retry_async_err_val_type_error() -> None:
    corrupted_on = "NotAnException"

    with pytest.raises(TypeError, match="'on' parameter must be an exception class or a tuple of exception classes"):
        @retry(max_attempts=2, on=corrupted_on)  # type: ignore
        async def faulty_func_async_err():
            pass


def test_chaos_retry_non_exception_class_in_tuple() -> None:
    corrupted_on = (ValueError, "NotAnException")

    with pytest.raises(TypeError, match="All elements in 'on' must be subclasses of BaseException"):
        @retry(max_attempts=2, on=corrupted_on)  # type: ignore
        def faulty_func_tuple():
            pass
