import pytest
from taipanstack.core.result import Ok, Err
from taipanstack.utils.rate_limit import rate_limit

def test_rate_limit_sync_nested_result():
    @rate_limit(max_calls=10, time_window=1.0)
    def my_func():
        return Err("Some business error")

    res = my_func()
    assert isinstance(res, Err)
    assert res.err_value == "Some business error"

    @rate_limit(max_calls=10, time_window=1.0)
    def my_func_ok():
        return Ok("Some business ok")

    res2 = my_func_ok()
    assert isinstance(res2, Ok)
    assert res2.ok_value == "Some business ok"

@pytest.mark.asyncio
async def test_rate_limit_async_nested_result():
    @rate_limit(max_calls=10, time_window=1.0)
    async def my_func():
        return Err("Some async business error")

    res = await my_func()
    assert isinstance(res, Err)
    assert res.err_value == "Some async business error"

    @rate_limit(max_calls=10, time_window=1.0)
    async def my_func_ok():
        return Ok("Some async business ok")

    res2 = await my_func_ok()
    assert isinstance(res2, Ok)
    assert res2.ok_value == "Some async business ok"
