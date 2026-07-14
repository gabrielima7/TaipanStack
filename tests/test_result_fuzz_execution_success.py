import hypothesis.strategies as st
from hypothesis import given

from taipanstack.core.result import (
    Err,
    Ok,
    Result,
    collect_results,
    safe,
    safe_from,
)


@given(st.text())
def test_result_ok_fuzz(value: str) -> None:
    res = Ok(value)
    assert res.is_ok() is True
    assert res.is_err() is False
    assert res.unwrap() == value
    assert res.unwrap_or("fallback") == value


@given(st.text())
def test_result_err_fuzz(value: str) -> None:
    err = ValueError(value)
    res = Err(err)
    assert res.is_ok() is False
    assert res.is_err() is True
    assert res.unwrap_or("fallback") == "fallback"
    assert res.err_value == err


@given(st.lists(st.text()))
def test_result_collect_results_all_ok_fuzz(
    values: list[str],
) -> None:
    results = [Ok(v) for v in values]
    res = collect_results(results)
    assert res.is_ok() is True
    assert res.unwrap() == values


@given(st.lists(st.text(), min_size=1), st.integers(min_value=0))
def test_result_collect_results_with_err_fuzz(
    values: list[str], err_index: int
) -> None:
    err_idx = err_index % len(values)
    results: list[Result[str, Exception]] = []
    for i, v in enumerate(values):
        if i == err_idx:
            results.append(Err(TypeError(v)))
        else:
            results.append(Ok(v))

    res = collect_results(results)
    assert res.is_err() is True
    assert isinstance(res.err_value, TypeError)


@given(st.lists(st.one_of(st.text(), st.integers())))
def test_result_safe_fuzz(values: list[object]) -> None:
    @safe
    def maybe_fail(v: object) -> str:
        if isinstance(v, int):
            raise TypeError("Int not allowed")
        return str(v)

    for v in values:
        res = maybe_fail(v)
        if isinstance(v, int):
            assert res.is_err() is True
        else:
            assert res.is_ok() is True
            assert res.unwrap() == str(v)


@given(st.lists(st.one_of(st.text(), st.integers())))
def test_result_safe_from_fuzz(values: list[object]) -> None:
    @safe_from(TypeError)
    def maybe_fail(v: object) -> str:
        if isinstance(v, int):
            raise TypeError("Int not allowed")
        return str(v)

    for v in values:
        res = maybe_fail(v)
        if isinstance(v, int):
            assert res.is_err() is True
            assert isinstance(res.err_value, TypeError)
        else:
            assert res.is_ok() is True
            assert res.unwrap() == str(v)
