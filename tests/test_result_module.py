"""Tests for the Result module (functional error handling)."""

import pytest

from taipanstack.core.result import (
    Err,
    Ok,
    Result,
    and_then_async,
    collect_results,
    map_async,
    safe,
    safe_from,
)


class TestOkErr:
    """Tests for basic Ok/Err functionality."""

    def test_ok_value(self) -> None:
        """Test Ok wraps value correctly."""
        result: Result[int, Exception] = Ok(42)
        assert result.is_ok()
        assert not result.is_err()
        assert result.ok_value == 42

    def test_err_value(self) -> None:
        """Test Err wraps error correctly."""
        error = ValueError("test error")
        result: Result[int, ValueError] = Err(error)
        assert result.is_err()
        assert not result.is_ok()
        assert result.err_value == error


class TestSafeDecorator:
    """Tests for the @safe decorator."""

    def test_safe_success(self) -> None:
        """Test safe decorator returns Ok on success."""

        @safe
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)
        assert result.is_ok()
        assert result.ok_value == 5

    def test_safe_exception(self) -> None:
        """Test safe decorator returns Err on exception."""

        @safe
        def divide(a: int, b: int) -> float:
            return a / b

        result = divide(10, 0)
        assert result.is_err()
        assert isinstance(result.err_value, ZeroDivisionError)

    def test_safe_basic_exception(self) -> None:
        """Test safe decorator returns Err on base Exception."""

        @safe
        def raise_exception() -> None:
            raise Exception("Basic exception occurred")  # noqa: TRY002

        result = raise_exception()
        assert result.is_err()
        err = result.err_value
        assert type(err) is Exception
        assert str(err) == "Basic exception occurred"

    def test_safe_preserves_function_metadata(self) -> None:
        """Test safe decorator preserves function name and docstring."""

        @safe
        def my_function() -> int:
            """My docstring."""
            return 42

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."


class TestSafeFromDecorator:
    """Tests for the @safe_from decorator."""

    def test_safe_from_catches_specified_exception(self) -> None:
        """Test safe_from catches specified exception types."""

        @safe_from(ValueError)
        def parse(s: str) -> int:
            return int(s)

        result = parse("not_a_number")
        assert result.is_err()
        assert isinstance(result.err_value, ValueError)

    def test_safe_from_propagates_unspecified_exception(self) -> None:
        """Test safe_from propagates unspecified exception types."""

        @safe_from(ValueError)
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

    def test_safe_from_multiple_types(self) -> None:
        """Test safe_from with multiple exception types."""

        @safe_from(ValueError, TypeError)
        def process(x: int | str) -> int:
            if isinstance(x, str):
                return int(x)
            raise TypeError("Expected string")

        result1 = process("abc")
        assert result1.is_err()
        assert isinstance(result1.err_value, ValueError)

        result2 = process(123)
        assert result2.is_err()
        assert isinstance(result2.err_value, TypeError)

    def test_safe_from_explicit_raise(self) -> None:
        """Test safe_from decorator catching explicitly raised exception."""

        @safe_from(ValueError)
        def process(data: str) -> int:
            raise ValueError("explicitly raised")

        result = process("abc")
        assert result.is_err()
        assert isinstance(result.err_value, ValueError)
        assert str(result.err_value) == "explicitly raised"

    def test_safe_from_inheritance(self) -> None:
        """Test safe_from catches subclasses of specified exceptions."""

        class SubValueError(ValueError):
            pass

        @safe_from(ValueError)
        def fail() -> None:
            raise SubValueError("subclass error")

        result = fail()
        assert result.is_err()
        assert isinstance(result.err_value, SubValueError)
        assert str(result.err_value) == "subclass error"


class TestCollectResults:
    """Tests for collect_results function."""

    def test_collect_all_ok(self) -> None:
        """Test collect_results with all Ok values."""
        results: list[Result[int, ValueError]] = [Ok(1), Ok(2), Ok(3)]
        collected = collect_results(results)
        assert collected.is_ok()
        assert collected.ok_value == [1, 2, 3]

    def test_collect_with_err(self) -> None:
        """Test collect_results stops at first Err."""
        results: list[Result[int, ValueError]] = [
            Ok(1),
            Err(ValueError("error")),
            Ok(3),
        ]
        collected = collect_results(results)
        assert collected.is_err()
        assert isinstance(collected.err_value, ValueError)
        assert str(collected.err_value) == "error"

    def test_collect_empty(self) -> None:
        """Test collect_results with empty list."""
        results: list[Result[int, ValueError]] = []
        collected = collect_results(results)
        assert collected.is_ok()
        assert collected.ok_value == []

    def test_collect_first_err_returned(self) -> None:
        """Test collect_results returns first Err encountered."""
        results: list[Result[int, ValueError]] = [
            Ok(1),
            Err(ValueError("first")),
            Err(ValueError("second")),
        ]
        collected = collect_results(results)
        assert collected.is_err()
        assert isinstance(collected.err_value, ValueError)
        assert str(collected.err_value) == "first"


class TestUnwrapOr:
    """Tests for unwrap_or function."""

    def test_unwrap_or_ok(self) -> None:
        """Test unwrap_or returns Ok value."""
        result: Result[int, ValueError] = Ok(42)
        assert result.unwrap_or(0) == 42

    def test_unwrap_or_err(self) -> None:
        """Test unwrap_or returns default on Err."""
        result: Result[int, ValueError] = Err(ValueError("error"))
        assert result.unwrap_or(0) == 0


class TestUnwrapOrElse:
    """Tests for unwrap_or_else function."""

    def test_unwrap_or_else_ok(self) -> None:
        """Test unwrap_or_else returns Ok value."""
        result: Result[int, ValueError] = Ok(42)
        assert result.unwrap_or_else(len) == 42

    def test_unwrap_or_else_err(self) -> None:
        """Test unwrap_or_else computes default from error."""
        result: Result[int, ValueError] = Err(ValueError("error"))
        assert result.unwrap_or_else(lambda e: len(str(e))) == 5

    def test_unwrap_or_else_with_exception(self) -> None:
        """Test unwrap_or_else with exception error type."""
        error = ValueError("test message")
        result: Result[int, ValueError] = Err(error)
        assert result.unwrap_or_else(lambda e: len(str(e))) == 12  # len("test message")


class TestMatchCase:
    """Tests for match/case pattern matching with Result."""

    def test_match_ok(self) -> None:
        """Test match/case with Ok value."""
        result: Result[int, ValueError] = Ok(42)
        match result:
            case Ok(value):
                assert value == 42
            case Err():
                pytest.fail("Should not match Err")

    def test_match_err(self) -> None:
        """Test match/case with Err value."""
        result: Result[int, ValueError] = Err(ValueError("error"))
        match result:
            case Ok():
                pytest.fail("Should not match Ok")
            case Err(error):
                assert isinstance(error, ValueError)
                assert str(error) == "error"


class TestSafeAsyncDecorator:
    """Tests for the @safe decorator with async functions."""

    @pytest.mark.asyncio
    async def test_safe_async_success(self) -> None:
        """Test safe decorator returns Ok on async success."""

        @safe
        async def async_add(a: int, b: int) -> int:
            return a + b

        result = await async_add(2, 3)
        assert result.is_ok()
        assert result.ok_value == 5

    @pytest.mark.asyncio
    async def test_safe_async_exception(self) -> None:
        """Test safe decorator returns Err on async exception."""

        @safe
        async def async_divide(a: int, b: int) -> float:
            return a / b

        result = await async_divide(10, 0)
        assert result.is_err()
        assert isinstance(result.err_value, ZeroDivisionError)

    @pytest.mark.asyncio
    async def test_safe_async_preserves_metadata(self) -> None:
        """Test safe decorator preserves async function name and docstring."""

        @safe
        async def my_async_function() -> int:
            """Async docstring."""
            return 42

        assert my_async_function.__name__ == "my_async_function"
        assert my_async_function.__doc__ == "Async docstring."

    @pytest.mark.asyncio
    async def test_safe_async_runtime_error(self) -> None:
        """Test safe decorator catches RuntimeError in async function."""

        @safe
        async def async_fail() -> str:
            msg = "something went wrong"
            raise RuntimeError(msg)

        result = await async_fail()
        assert result.is_err()
        assert isinstance(result.err_value, RuntimeError)

    @pytest.mark.asyncio
    async def test_safe_async_basic_exception(self) -> None:
        """Test safe decorator returns Err on base Exception in async function."""

        @safe
        async def async_raise_exception() -> None:
            raise Exception("Basic async exception occurred")  # noqa: TRY002

        result = await async_raise_exception()
        assert result.is_err()
        err = result.err_value
        assert type(err) is Exception
        assert str(err) == "Basic async exception occurred"


class TestMapAsync:
    """Tests for map_async function."""

    @pytest.mark.asyncio
    async def test_map_async_ok(self) -> None:
        """Test map_async with Ok value."""

        async def double(x: int) -> int:
            return x * 2

        result: Result[int, ValueError] = Ok(21)
        mapped = await map_async(result, double)
        assert mapped.is_ok()
        assert mapped.ok_value == 42

    @pytest.mark.asyncio
    async def test_map_async_err(self) -> None:
        """Test map_async with Err value."""

        async def double(x: int) -> int:
            return x * 2

        result: Result[int, ValueError] = Err(ValueError("error"))
        mapped: Result[int, ValueError] = await map_async(result, double)
        assert mapped.is_err()
        assert isinstance(mapped.err_value, ValueError)


class TestAndThenAsync:
    """Tests for and_then_async function."""

    @pytest.mark.asyncio
    async def test_and_then_async_ok_to_ok(self) -> None:
        """Test and_then_async mapping Ok to Ok."""

        async def process(x: int) -> Result[str, ValueError]:
            return Ok(str(x * 2))

        result: Result[int, ValueError] = Ok(21)
        chained = await and_then_async(result, process)
        assert chained.is_ok()
        assert chained.ok_value == "42"

    @pytest.mark.asyncio
    async def test_and_then_async_ok_to_err(self) -> None:
        """Test and_then_async mapping Ok to Err."""

        async def process(x: int) -> Result[str, ValueError]:
            return Err(ValueError("validation failed"))

        result: Result[int, ValueError] = Ok(21)
        chained = await and_then_async(result, process)
        assert chained.is_err()
        assert isinstance(chained.err_value, ValueError)

    @pytest.mark.asyncio
    async def test_and_then_async_err(self) -> None:
        """Test and_then_async with Err value skips execution."""

        executed = False

        async def process(x: int) -> Result[str, ValueError]:
            nonlocal executed
            executed = True
            return Ok(str(x))

        result: Result[int, ValueError] = Err(ValueError("initial error"))
        chained: Result[str, ValueError] = await and_then_async(result, process)
        assert chained.is_err()
        assert isinstance(chained.err_value, ValueError)
        assert not executed


class TestSafeFromAsyncDecorator:
    @pytest.mark.asyncio
    async def test_safe_from_async_success(self) -> None:
        @safe_from(ValueError)
        async def process(x: int) -> int:
            return x * 2

        result = await process(5)
        assert result == Ok(10)

    @pytest.mark.asyncio
    async def test_safe_from_async_exception(self) -> None:
        @safe_from(ValueError)
        async def process(x: int) -> int:
            raise ValueError("invalid")

        result = await process(5)
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ValueError)

    @pytest.mark.asyncio
    async def test_safe_from_async_propagates_unspecified(self) -> None:
        @safe_from(ValueError)
        async def process(x: int) -> int:
            raise TypeError("invalid type")

        with pytest.raises(TypeError):
            await process(5)
