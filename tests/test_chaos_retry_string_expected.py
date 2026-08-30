import pytest

from taipanstack.core.result import Ok
from taipanstack.resilience.retry import RetryError, retry


def test_chaos_retry_string_max_attempts_expected() -> None:
    @retry(max_attempts="3")  # type: ignore
    def my_func() -> Ok[str]:
        return Ok("success")

    assert my_func().unwrap() == "success"


@pytest.mark.asyncio
async def test_chaos_retry_string_max_attempts_async_expected() -> None:
    @retry(max_attempts="3")  # type: ignore
    async def my_func() -> Ok[str]:
        return Ok("success")

    res = await my_func()
    assert res.unwrap() == "success"


def test_chaos_retry_string_max_attempts_failure_expected() -> None:
    @retry(max_attempts="3", on=ValueError)  # type: ignore
    def my_func() -> Ok[str]:
        raise ValueError("test")

    with pytest.raises(RetryError) as exc_info:
        my_func()

    assert exc_info.value.attempts == 3
    assert isinstance(exc_info.value.attempts, int)


@pytest.mark.asyncio
async def test_chaos_retry_string_max_attempts_async_failure_expected() -> None:
    @retry(max_attempts="3", on=ValueError)  # type: ignore
    async def my_func() -> Ok[str]:
        raise ValueError("test")

    with pytest.raises(RetryError) as exc_info:
        await my_func()

    assert exc_info.value.attempts == 3
    assert isinstance(exc_info.value.attempts, int)
