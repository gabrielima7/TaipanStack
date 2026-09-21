from collections.abc import Iterable
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok, collect_results, safe, safe_from


@given(st.lists(st.integers() | st.text() | st.floats()))
def test_fuzz_core_result_operations_collect_results_all_ok_list(values: list[Any]) -> None:
    results = [Ok(v) for v in values]
    collected = collect_results(results)
    assert not collected.is_err()
    assert collected.unwrap() == values

@given(st.lists(st.integers() | st.text() | st.floats()))
def test_fuzz_core_result_operations_collect_results_all_ok_tuple(values: list[Any]) -> None:
    results = tuple(Ok(v) for v in values)
    collected = collect_results(results)
    assert not collected.is_err()
    assert collected.unwrap() == values

@given(st.lists(st.integers() | st.text() | st.floats()))
def test_fuzz_core_result_operations_collect_results_all_ok_generator(values: list[Any]) -> None:
    def gen() -> Iterable[Ok[Any]]:
        for v in values:
            yield Ok(v)

    collected = collect_results(gen())
    assert not collected.is_err()
    assert collected.unwrap() == values

@given(st.lists(st.integers(), min_size=1), st.text())
def test_fuzz_core_result_operations_collect_results_with_err_list(ok_values: list[int], err_value: str) -> None:
    results: list[Ok[int] | Err[ValueError]] = [Ok(v) for v in ok_values]
    err = Err(ValueError(err_value))
    results.append(err)

    collected = collect_results(results)
    assert collected.is_err()
    assert collected.unwrap_err() == err.unwrap_err()

@given(st.integers())
def test_fuzz_core_result_operations_safe_sync_ok(val: int) -> None:
    @safe
    def dummy(x: int) -> int:
        return x * 2

    res = dummy(val)
    assert not res.is_err()
    assert res.unwrap() == val * 2

@given(st.text())
def test_fuzz_core_result_operations_safe_sync_err(val: str) -> None:
    @safe
    def dummy(x: str) -> int:
        raise ValueError(x)

    res = dummy(val)
    assert res.is_err()
    assert isinstance(res.unwrap_err(), ValueError)
    assert str(res.unwrap_err()) == val

@pytest.mark.asyncio
@given(st.integers())
async def test_fuzz_core_result_operations_safe_async_ok(val: int) -> None:
    @safe
    async def dummy(x: int) -> int:
        return x * 2

    res = await dummy(val)
    assert not res.is_err()
    assert res.unwrap() == val * 2

@pytest.mark.asyncio
@given(st.text())
async def test_fuzz_core_result_operations_safe_async_err(val: str) -> None:
    @safe
    async def dummy(x: str) -> int:
        raise ValueError(x)

    res = await dummy(val)
    assert res.is_err()
    assert isinstance(res.unwrap_err(), ValueError)
    assert str(res.unwrap_err()) == val


@given(st.integers())
def test_fuzz_core_result_operations_safe_from_sync_ok(val: int) -> None:
    @safe_from(ValueError)
    def dummy(x: int) -> int:
        return x * 2

    res = dummy(val)
    assert not res.is_err()
    assert res.unwrap() == val * 2

@given(st.text())
def test_fuzz_core_result_operations_safe_from_sync_err_caught(val: str) -> None:
    @safe_from(ValueError)
    def dummy(x: str) -> int:
        raise ValueError(x)

    res = dummy(val)
    assert res.is_err()
    assert isinstance(res.unwrap_err(), ValueError)
    assert str(res.unwrap_err()) == val

@given(st.text())
def test_fuzz_core_result_operations_safe_from_sync_err_uncaught(val: str) -> None:
    @safe_from(ValueError)
    def dummy(x: str) -> int:
        raise TypeError(x)

    with pytest.raises(TypeError) as exc:
        dummy(val)
    assert str(exc.value) == val

@pytest.mark.asyncio
@given(st.integers())
async def test_fuzz_core_result_operations_safe_from_async_ok(val: int) -> None:
    @safe_from(ValueError)
    async def dummy(x: int) -> int:
        return x * 2

    res = await dummy(val)
    assert not res.is_err()
    assert res.unwrap() == val * 2

@pytest.mark.asyncio
@given(st.text())
async def test_fuzz_core_result_operations_safe_from_async_err_caught(val: str) -> None:
    @safe_from(ValueError)
    async def dummy(x: str) -> int:
        raise ValueError(x)

    res = await dummy(val)
    assert res.is_err()
    assert isinstance(res.unwrap_err(), ValueError)
    assert str(res.unwrap_err()) == val

@pytest.mark.asyncio
@given(st.text())
async def test_fuzz_core_result_operations_safe_from_async_err_uncaught(val: str) -> None:
    @safe_from(ValueError)
    async def dummy(x: str) -> int:
        raise TypeError(x)

    with pytest.raises(TypeError) as exc:
        await dummy(val)
    assert str(exc.value) == val
