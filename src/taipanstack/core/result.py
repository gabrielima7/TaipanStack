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
    >>> if isinstance(result, Err):
    ...     print(f"Error: {result.err_value}")
    ... else:
    ...     print(f"Result: {result.unwrap()}")
    Error: division by zero

"""

import functools
import inspect
from collections.abc import Awaitable, Callable, Iterable
from typing import ParamSpec, Protocol, TypeVar, cast, overload

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
]

P = ParamSpec("P")
T = TypeVar("T")
E = TypeVar("E", bound=Exception)
E_co = TypeVar("E_co", bound=Exception, covariant=True)
U = TypeVar("U")


@overload
def safe(
    func: Callable[P, T],
) -> Callable[P, Result[T, Exception]]: ...


@overload
def safe(
    func: Callable[P, Awaitable[T]],
) -> Callable[P, Awaitable[Result[T, Exception]]]: ...


def safe(
    func: Callable[P, T] | Callable[P, Awaitable[T]],
) -> Callable[P, Result[T, Exception]] | Callable[P, Awaitable[Result[T, Exception]]]:
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
    # Pre-cache constructors for minor speedup in tight loops
    # (LOAD_DEREF is faster than LOAD_GLOBAL)
    ok_cls = Ok
    err_cls = Err

    if inspect.iscoroutinefunction(func):
        # Cast once here to satisfy mypy inside the closure
        func_coro = cast(Callable[P, Awaitable[T]], func)

        @functools.wraps(func)
        async def async_wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> Result[T, Exception]:
            try:
                return ok_cls(await func_coro(*args, **kwargs))
            except Exception as e:
                return err_cls(e)

        return cast(Callable[P, Awaitable[Result[T, Exception]]], async_wrapper)

    # Cast once here to satisfy mypy inside the closure
    func_sync = cast(Callable[P, T], func)

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, Exception]:
        try:
            return ok_cls(func_sync(*args, **kwargs))
        except Exception as e:
            return err_cls(e)

    return cast(Callable[P, Result[T, Exception]], wrapper)


class SafeFromDecorator(Protocol[E_co]):
    """Protocol for safe_from decorator."""

    @overload
    def __call__(self, func: Callable[P, T]) -> Callable[P, Result[T, E_co]]: ...

    @overload
    def __call__(
        self,
        func: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[Result[T, E_co]]]: ...


def safe_from(
    *exception_types: type[E],
) -> SafeFromDecorator[E]:
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

    def decorator(
        func: Callable[P, T] | Callable[P, Awaitable[T]],
    ) -> Callable[P, Result[T, E]] | Callable[P, Awaitable[Result[T, E]]]:
        if inspect.iscoroutinefunction(func):
            func_coro = cast(Callable[P, Awaitable[T]], func)

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
                try:
                    return Ok(await func_coro(*args, **kwargs))
                except exception_types as e:
                    return Err(e)

            return cast(Callable[P, Awaitable[Result[T, E]]], async_wrapper)

        func_sync = cast(Callable[P, T], func)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
            try:
                return Ok(func_sync(*args, **kwargs))
            except exception_types as e:
                return Err(e)

        return cast(Callable[P, Result[T, E]], wrapper)

    return cast(SafeFromDecorator[E], decorator)


def _collect_list(
    results: list[Result[T, E]] | tuple[Result[T, E], ...],
) -> Result[list[T], E] | None:
    try:
        # We use a runtime # type: ignore to bypass mypy's strict check
        # on the AttributeError strategy for extreme performance on the hot path
        return Ok([r.ok_value for r in results])  # type: ignore[union-attr]
    except AttributeError:
        # Type-bound failure. If an object didn't have ok_value, we fall back
        # to the safer (but slower) _collect_iterable to raise a proper TypeError.
        return None


def _collect_iterable(
    results: Iterable[Result[T, E]],
) -> Result[list[T], E]:
    """Collect an iterable of Results iteratively."""
    ok_cls = Ok
    err_cls = Err
    values: list[T] = []
    append = values.append
    for result in results:
        # We use explicit type checks (isinstance) but pre-cache the constructors.
        # type(result) is ok_cls would be even faster but breaks subclassing.
        if isinstance(result, ok_cls):
            append(result.ok_value)
        elif isinstance(result, err_cls):
            return result
        else:
            raise TypeError(f"Expected Result, got {type(result)}")
    return ok_cls(values)


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
    if isinstance(results, (list, tuple)):
        optimized_res = _collect_list(results)
        if optimized_res is not None:
            return optimized_res

    return _collect_iterable(results)


@overload
async def map_async(
    result: Ok[T],
    func: Callable[[T], Awaitable[U]],
) -> Result[U, E]: ...


@overload
async def map_async(
    result: Err[E],
    func: Callable[[T], Awaitable[U]],
) -> Err[E]: ...


@overload
async def map_async(
    result: Result[T, E],
    func: Callable[[T], Awaitable[U]],
) -> Result[U, E]: ...


async def map_async(
    result: Result[T, E],
    func: Callable[[T], Awaitable[U]],
) -> Result[U, E]:
    """Asynchronously apply a function to the value of an Ok result.

    If the result is Err, returns it unchanged.

    Args:
        result: The Result to process.
        func: Awaitable function to apply to the Ok value.

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
    func: Callable[[T], Awaitable[Result[U, E]]],
) -> Result[U, E]: ...


@overload
async def and_then_async(
    result: Err[E],
    func: Callable[[T], Awaitable[Result[U, E]]],
) -> Err[E]: ...


@overload
async def and_then_async(
    result: Result[T, E],
    func: Callable[[T], Awaitable[Result[U, E]]],
) -> Result[U, E]: ...


async def and_then_async(
    result: Result[T, E],
    func: Callable[[T], Awaitable[Result[U, E]]],
) -> Result[U, E]:
    """Asynchronously chain operations that return Results.

    If the result is Ok, asynchronously applies `func` and returns its Result.
    If the result is Err, returns it unchanged.

    Args:
        result: The Result to process.
        func: Awaitable function taking the Ok value and returning a new Result.

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
