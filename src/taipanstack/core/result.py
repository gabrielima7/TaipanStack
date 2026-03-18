"""
Result type utilities for functional error handling.

Provides Rust-style Result types (Ok/Err) for explicit error handling,
avoiding exceptions for expected failure cases. This promotes safer,
more predictable code.

Example:
    >>> from taipanstack.core.result import safe, Ok, Err
    >>> @safe
    ... def divide(a: int, b: int) -> float:
    ...     if b == 0:
    ...         raise ValueError("division by zero")
    ...     return a / b
    >>> result = divide(10, 0)
    >>> match result:
    ...     case Err(e):
    ...         print(f"Error: {e}")
    ...     case Ok(value):
    ...         print(f"Result: {value}")
    Error: division by zero

"""

import functools
import inspect
from collections.abc import Callable, Coroutine, Iterable
from typing import Any, ParamSpec, TypeVar, overload

from result import Err, Ok, Result

__all__ = [
    "Err",
    "Ok",
    "Result",
    "and_then_async",
    "collect_results",
    "map_async",
    "safe",
    "safe_from",
    "unwrap_or",
    "unwrap_or_else",
]

P = ParamSpec("P")
T = TypeVar("T")
E = TypeVar("E", bound=Exception)
U = TypeVar("U")


@overload
def safe(
    func: Callable[P, T],
) -> Callable[P, Result[T, Exception]]: ...  # pragma: no cover


@overload
def safe(
    func: Callable[P, Coroutine[Any, Any, T]],
) -> Callable[P, Coroutine[Any, Any, Result[T, Exception]]]: ...  # pragma: no cover


def safe(
    func: Callable[P, T] | Callable[P, Coroutine[Any, Any, T]],
) -> (
    Callable[P, Result[T, Exception]]
    | Callable[P, Coroutine[Any, Any, Result[T, Exception]]]
):
    """Wrap a sync or async function to convert exceptions into Err results.

    Detect whether *func* is a coroutine function and choose the
    appropriate wrapper so that ``await``-able functions remain
    ``await``-able and synchronous functions stay synchronous.

    Args:
        func: The sync or async function to wrap.

    Returns:
        A wrapped function that returns ``Result[T, Exception]``
        (or a coroutine resolving to one).

    Example:
        >>> @safe
        ... def parse_int(s: str) -> int:
        ...     return int(s)
        >>> parse_int("42")
        Ok(42)
        >>> parse_int("invalid")
        Err(ValueError("invalid literal for int()..."))

    """
    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> Result[T, Exception]:
            try:
                return Ok(await func(*args, **kwargs))
            except Exception as e:
                return Err(e)

        return async_wrapper

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, Exception]:
        try:
            return Ok(func(*args, **kwargs))  # type: ignore[arg-type]
        except Exception as e:
            return Err(e)

    return wrapper


def safe_from(
    *exception_types: type[E],
) -> Callable[[Callable[P, T]], Callable[P, Result[T, E]]]:
    """Decorator factory to catch specific exceptions as Err.

    Only catches specified exception types; others propagate normally.

    Args:
        *exception_types: Exception types to convert to Err.

    Returns:
        Decorator that wraps function with selective error handling.

    Example:
        >>> @safe_from(ValueError, TypeError)
        ... def process(data: str) -> int:
        ...     return int(data)
        >>> process("abc")
        Err(ValueError(...))

    """

    def decorator(func: Callable[P, T]) -> Callable[P, Result[T, E]]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
            try:
                return Ok(func(*args, **kwargs))
            except exception_types as e:
                return Err(e)

        return wrapper

    return decorator


def collect_results(
    results: Iterable[Result[T, E]],
) -> Result[list[T], E]:
    """Collect an iterable of Results into a single Result.

    If all results are Ok, returns Ok with list of values.
    If any result is Err, returns the first Err encountered.

    Args:
        results: Iterable of Result objects.

    Returns:
        Ok(list[T]) if all are Ok, otherwise first Err.

    Example:
        >>> collect_results([Ok(1), Ok(2), Ok(3)])
        Ok([1, 2, 3])
        >>> collect_results([Ok(1), Err("fail"), Ok(3)])
        Err("fail")

    """
    values: list[T] = []
    append = values.append
    for r in results:
        try:
            append(r.ok_value)
        except AttributeError:
            return r
    return Ok(values)


@overload
def unwrap_or(result: Ok[T], default: U) -> T: ...  # pragma: no cover


@overload
def unwrap_or(result: Err[E], default: U) -> U: ...  # pragma: no cover


@overload
def unwrap_or(result: Result[T, E], default: U) -> T | U: ...  # pragma: no cover


def unwrap_or(result: Result[T, E], default: U) -> T | U:
    """Extract value from Result or return default.

    Args:
        result: The Result to unwrap.
        default: Default value if result is Err.

    Returns:
        The Ok value or the default.

    Example:
        >>> unwrap_or(Ok(42), 0)
        42
        >>> unwrap_or(Err("error"), 0)
        0

    """
    if isinstance(result, Ok):
        return result.ok_value
    return default


@overload
def unwrap_or_else(
    result: Ok[T],
    default_fn: Callable[[E], U],
) -> T: ...  # pragma: no cover


@overload
def unwrap_or_else(
    result: Err[E],
    default_fn: Callable[[E], U],
) -> U: ...  # pragma: no cover


@overload
def unwrap_or_else(
    result: Result[T, E],
    default_fn: Callable[[E], U],
) -> T | U: ...  # pragma: no cover


def unwrap_or_else(
    result: Result[T, E],
    default_fn: Callable[[E], U],
) -> T | U:
    """Extract value from Result or compute default from error.

    Args:
        result: The Result to unwrap.
        default_fn: Function to compute default from error.

    Returns:
        The Ok value or computed default.

    Example:
        >>> unwrap_or_else(Ok(42), lambda e: 0)
        42
        >>> unwrap_or_else(Err(ValueError("x")), lambda e: len(str(e)))
        1

    """
    if isinstance(result, Ok):
        return result.ok_value
    return default_fn(result.err_value)


@overload
async def map_async(
    result: Ok[T],
    func: Callable[[T], Coroutine[Any, Any, U]],
) -> Result[U, E]: ...  # pragma: no cover


@overload
async def map_async(
    result: Err[E],
    func: Callable[[T], Coroutine[Any, Any, U]],
) -> Err[E]: ...  # pragma: no cover


@overload
async def map_async(
    result: Result[T, E],
    func: Callable[[T], Coroutine[Any, Any, U]],
) -> Result[U, E]: ...  # pragma: no cover


async def map_async(
    result: Result[T, E],
    func: Callable[[T], Coroutine[Any, Any, U]],
) -> Result[U, E]:
    """Asynchronously apply a function to the value of an Ok result.

    If the result is Err, returns it unchanged.

    Args:
        result: The Result to process.
        func: Coroutine function to apply to the Ok value.

    Returns:
        New Result containing the processed value or original error.

    Example:
        >>> async def process(x: int) -> str:
        ...     return str(x * 2)
        >>> await map_async(Ok(5), process)
        Ok('10')
        >>> await map_async(Err("fail"), process)
        Err('fail')

    """
    if isinstance(result, Ok):
        return Ok(await func(result.ok_value))
    return result


@overload
async def and_then_async(
    result: Ok[T],
    func: Callable[[T], Coroutine[Any, Any, Result[U, E]]],
) -> Result[U, E]: ...  # pragma: no cover


@overload
async def and_then_async(
    result: Err[E],
    func: Callable[[T], Coroutine[Any, Any, Result[U, E]]],
) -> Err[E]: ...  # pragma: no cover


@overload
async def and_then_async(
    result: Result[T, E],
    func: Callable[[T], Coroutine[Any, Any, Result[U, E]]],
) -> Result[U, E]: ...  # pragma: no cover


async def and_then_async(
    result: Result[T, E],
    func: Callable[[T], Coroutine[Any, Any, Result[U, E]]],
) -> Result[U, E]:
    """Asynchronously chain operations that return Results.

    If the result is Ok, asynchronously applies `func` and returns its Result.
    If the result is Err, returns it unchanged.

    Args:
        result: The Result to process.
        func: Coroutine function taking the Ok value and returning a new Result.

    Returns:
        The new Result from `func` or the original error.

    Example:
        >>> async def fetch_user(uid: int) -> Result[str, ValueError]:
        ...     if uid == 1:
        ...         return Ok("Alice")
        ...     return Err(ValueError("User not found"))
        >>> await and_then_async(Ok(1), fetch_user)
        Ok('Alice')
        >>> await and_then_async(Ok(2), fetch_user)
        Err(ValueError('User not found'))
        >>> await and_then_async(Err(ValueError("No DB")), fetch_user)
        Err(ValueError('No DB'))

    """
    if isinstance(result, Ok):
        return await func(result.ok_value)
    return result
