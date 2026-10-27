from collections.abc import Iterable

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from result import Err, Ok, Result

from taipanstack.core.result import (
    and_then_async,
    collect_results,
    map_async,
    safe,
    safe_from,
)

# Define basic types and strategies
any_obj = st.one_of(
    st.integers(), st.floats(allow_nan=False), st.text(), st.booleans(), st.none()
)
err_obj = st.builds(Exception, st.text())
ok_strategy = st.builds(Ok, any_obj)
err_strategy = st.builds(Err, err_obj)
result_strategy = st.one_of(ok_strategy, err_strategy)

# Nested strategies
nested_ok_strategy = st.builds(
    Ok, st.recursive(any_obj, lambda x: st.builds(Ok, x), max_leaves=10)
)

# Massive list of Results
massive_result_list = st.lists(result_strategy, min_size=10, max_size=100)


@given(value=any_obj)
def test_fuzz_result_ok_creation(value: object) -> None:
    ok = Ok(value)
    assert ok.ok_value == value
    assert ok.unwrap() == value
    assert ok.is_ok()


@given(exc=err_obj)
def test_fuzz_result_err_creation(exc: Exception) -> None:
    err = Err(exc)
    assert err.err_value == exc
    assert err.is_err()


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.too_slow],
    deadline=None,
)
@given(results=massive_result_list)
def test_fuzz_result_collect_results_massive_list(
    results: list[Result[object, Exception]],
) -> None:
    collected = collect_results(results)

    has_err = any(isinstance(r, Err) for r in results)

    if has_err:
        assert isinstance(collected, Err)
        # Verify it's the first Err
        first_err = next(r for r in results if isinstance(r, Err))
        assert collected.err_value == first_err.err_value
    else:
        assert isinstance(collected, Ok)
        assert len(collected.ok_value) == len(results)


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.too_slow],
    deadline=None,
)
@given(results=massive_result_list)
def test_fuzz_result_collect_results_massive_tuple(
    results: list[Result[object, Exception]],
) -> None:
    tup_results = tuple(results)
    collected = collect_results(tup_results)

    has_err = any(isinstance(r, Err) for r in tup_results)

    if has_err:
        assert isinstance(collected, Err)
        first_err = next(r for r in tup_results if isinstance(r, Err))
        assert collected.err_value == first_err.err_value
    else:
        assert isinstance(collected, Ok)
        assert len(collected.ok_value) == len(tup_results)


@given(results=st.lists(result_strategy, max_size=50))
def test_fuzz_result_collect_results_iterable(
    results: list[Result[object, Exception]],
) -> None:
    # Use a generator to test iterable path
    def gen() -> Iterable[Result[object, Exception]]:
        yield from results

    collected = collect_results(gen())

    has_err = any(isinstance(r, Err) for r in results)
    if has_err:
        assert isinstance(collected, Err)
    else:
        assert isinstance(collected, Ok)
        assert len(collected.ok_value) == len(results)


def test_fuzz_result_collect_results_invalid_type() -> None:
    with pytest.raises(TypeError):
        collect_results([Ok(1), "not a result"])  # type: ignore


@given(value=any_obj)
def test_fuzz_result_safe_sync_ok(value: object) -> None:
    @safe
    def sync_func(x: object) -> object:
        return x

    result = sync_func(value)
    assert isinstance(result, Ok)
    assert result.ok_value == value


@given(msg=st.text())
def test_fuzz_result_safe_sync_err(msg: str) -> None:
    @safe
    def sync_fail(m: str) -> str:
        raise ValueError(m)

    result = sync_fail(msg)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)
    assert str(result.err_value) == msg


@pytest.mark.asyncio
@given(value=any_obj)
async def test_fuzz_result_safe_async_ok(value: object) -> None:
    @safe
    async def async_func(x: object) -> object:
        return x

    result = await async_func(value)
    assert isinstance(result, Ok)
    assert result.ok_value == value


@pytest.mark.asyncio
@given(msg=st.text())
async def test_fuzz_result_safe_async_err(msg: str) -> None:
    @safe
    async def async_fail(m: str) -> str:
        raise ValueError(m)

    result = await async_fail(msg)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)


@given(value=any_obj)
def test_fuzz_result_safe_from_sync_handled(value: object) -> None:
    @safe_from(ValueError)
    def sync_fail(x: object) -> object:
        raise ValueError("handled")

    result = sync_fail(value)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)


@given(value=any_obj)
def test_fuzz_result_safe_from_sync_unhandled(value: object) -> None:
    @safe_from(TypeError)
    def sync_fail(x: object) -> object:
        raise ValueError("unhandled")

    with pytest.raises(ValueError):
        sync_fail(value)


@pytest.mark.asyncio
@given(value=any_obj)
async def test_fuzz_result_safe_from_async_handled(value: object) -> None:
    @safe_from(ValueError)
    async def async_fail(x: object) -> object:
        raise ValueError("handled")

    result = await async_fail(value)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, ValueError)


@pytest.mark.asyncio
@given(res=result_strategy)
async def test_fuzz_result_map_async(res: Result[object, Exception]) -> None:
    async def process(x: object) -> str:
        return f"processed_{x}"

    mapped = await map_async(res, process)

    if isinstance(res, Ok):
        assert isinstance(mapped, Ok)
        assert mapped.ok_value == f"processed_{res.ok_value}"
    else:
        assert isinstance(mapped, Err)
        assert mapped.err_value == res.err_value


@pytest.mark.asyncio
@given(res=result_strategy)
async def test_fuzz_result_and_then_async(res: Result[object, Exception]) -> None:
    async def process(x: object) -> Result[str, Exception]:
        if isinstance(x, str):
            return Ok(x + "_ok")
        return Err(TypeError("not str"))

    chained = await and_then_async(res, process)

    if isinstance(res, Err):
        assert isinstance(chained, Err)
        assert chained.err_value == res.err_value
    elif isinstance(res.ok_value, str):
        assert isinstance(chained, Ok)
        assert chained.ok_value == res.ok_value + "_ok"
    else:
        assert isinstance(chained, Err)
        assert isinstance(chained.err_value, TypeError)
