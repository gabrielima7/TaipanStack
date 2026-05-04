"""
Resilience Orchestrator — compose multiple patterns into a pipeline.

Provides a fluent builder to combine bulkhead, circuit breaker,
retry, timeout, and fallback into a single execution pipeline.

Execution order: bulkhead → circuit breaker → retry → timeout → fn → fallback.
"""

from __future__ import annotations

import asyncio
import logging
import math
from collections.abc import Awaitable, Callable
from typing import Generic, ParamSpec, TypeVar, cast

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.bulkhead import Bulkhead, BulkheadFullError
from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
)
from taipanstack.resilience.retry import RetryConfig, calculate_delay

logger = logging.getLogger("taipanstack.resilience.adaptive.orchestrator")

T = TypeVar("T")
E = TypeVar("E", bound=Exception)
P = ParamSpec("P")


class ResilienceOrchestrator(Generic[T]):
    """Compose resilience patterns into a single pipeline.

    Provides a fluent builder API to add patterns in order.
    Execution proceeds through each configured layer.

    Args:
        name: Pipeline name for logging.

    Example:
        >>> orch = (
        ...     ResilienceOrchestrator("api")
        ...     .with_bulkhead(max_concurrent=5)
        ...     .with_circuit_breaker(breaker)
        ...     .with_retry(RetryConfig(max_attempts=3))
        ...     .with_timeout(10.0)
        ...     .with_fallback({"status": "cached"})
        ... )
        >>> result = await orch.execute(call_api, endpoint)

    """

    def __init__(self, name: str = "default") -> None:
        """Initialize the orchestrator.

        Args:
            name: Pipeline name.

        """
        self.name = name
        self._bulkhead: Bulkhead | None = None
        self._breaker: CircuitBreaker | None = None
        self._adaptive_breaker: AdaptiveCircuitBreaker | None = None
        self._retry_config: RetryConfig | None = None
        self._adaptive_retry: AdaptiveRetry | None = None
        self._timeout: float | None = None
        self._fallback_value: T | object = _SENTINEL

    def with_bulkhead(
        self,
        max_concurrent: int = 10,
        max_queue: int = 50,
        timeout: float = 30.0,
    ) -> ResilienceOrchestrator[T]:
        """Add a bulkhead concurrency limiter.

        Args:
            max_concurrent: Max concurrent executions.
            max_queue: Max queued callers.
            timeout: Permit acquisition timeout.

        Returns:
            self for chaining.

        """
        if not math.isfinite(timeout) or timeout < 0:
            raise ValueError("timeout must be a finite non-negative number")
        self._bulkhead = Bulkhead(
            f"{self.name}-bulkhead",
            max_concurrent=max_concurrent,
            max_queue=max_queue,
            timeout=timeout,
        )
        return self

    def with_circuit_breaker(
        self,
        breaker: CircuitBreaker | AdaptiveCircuitBreaker,
    ) -> ResilienceOrchestrator[T]:
        """Add a circuit breaker.

        Args:
            breaker: Standard or adaptive circuit breaker.

        Returns:
            self for chaining.

        """
        if isinstance(breaker, AdaptiveCircuitBreaker):
            self._adaptive_breaker = breaker
            self._breaker = None
        else:
            self._breaker = breaker
        return self

    def with_retry(
        self,
        config: RetryConfig | AdaptiveRetry,
    ) -> ResilienceOrchestrator[T]:
        """Add retry logic.

        Args:
            config: Standard retry config or adaptive retry.

        Returns:
            self for chaining.

        """
        if isinstance(config, AdaptiveRetry):
            self._adaptive_retry = config
            self._retry_config = config.to_retry_config()
        else:
            self._retry_config = config
        return self

    def with_timeout(self, seconds: float) -> ResilienceOrchestrator[T]:
        """Add a timeout.

        Args:
            seconds: Maximum execution time.

        Returns:
            self for chaining.

        """
        if not math.isfinite(seconds) or seconds < 0:
            raise ValueError("timeout must be a finite non-negative number")
        self._timeout = seconds
        return self

    def with_fallback(self, value: T) -> ResilienceOrchestrator[T]:
        """Add a fallback value for failures.

        Args:
            value: Value to return on failure.

        Returns:
            self for chaining.

        """
        self._fallback_value = value
        return self

    async def execute(
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Exception]:
        """Execute the function through the resilience pipeline.

        Order: bulkhead → circuit breaker → retry → timeout → fn → fallback.

        Args:
            fn: Async callable to execute.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            ``Ok(result)`` on success, ``Err`` on failure.

        """
        # Layer 1: Bulkhead — use semaphore directly to avoid double-wrapping
        if self._bulkhead is not None:
            bh = self._bulkhead
            if bh.queued >= bh._max_queue:
                result: Result[T, Exception] = Err(
                    BulkheadFullError(bh.name, bh._max_concurrent, bh._max_queue)
                )
                return self._apply_fallback(result)

            bh._queued += 1
            try:
                try:
                    await asyncio.wait_for(
                        bh._semaphore.acquire(),
                        timeout=bh._timeout,
                    )
                except TimeoutError:
                    return self._apply_fallback(
                        Err(
                            TimeoutError(
                                f"Bulkhead '{bh.name}' timed out after {bh._timeout}s"
                            )
                        )
                    )
                except (RuntimeError, OSError, MemoryError) as e:
                    return self._apply_fallback(
                        Err(RuntimeError(f"Resource exhaustion: {e!s}"))
                    )
            finally:
                bh._queued -= 1

            bh._active += 1
            try:
                return await self._execute_inner(fn, *args, **kwargs)
            finally:
                bh._active -= 1
                bh._semaphore.release()

        return await self._execute_inner(fn, *args, **kwargs)

    def _evaluate_circuit_breaker(self) -> Result[T, Exception] | None:
        """Check if execution is allowed by the circuit breaker."""
        if self._adaptive_breaker is not None:
            if not self._adaptive_breaker.should_allow():
                return Err(
                    CircuitBreakerError(
                        f"Circuit '{self._adaptive_breaker.name}' is open",
                        state=self._adaptive_breaker.state,
                    )
                )
        elif self._breaker is not None and not self._breaker._should_attempt():
            return Err(
                CircuitBreakerError(
                    f"Circuit '{self._breaker.name}' is open",
                    state=self._breaker.state,
                )
            )
        return None

    def _record_success_outcome(self, attempt: int) -> None:
        """Record a successful execution outcome."""
        if self._adaptive_breaker is not None:
            self._adaptive_breaker.record_success()
        elif self._breaker is not None:
            self._breaker._record_success()

        if self._adaptive_retry is not None:
            self._adaptive_retry.record_outcome(attempt, True, 0.0)

    def _record_failure_outcome(self, error: Exception, attempt: int) -> None:
        """Record a failed execution outcome."""
        if self._adaptive_breaker is not None:
            self._adaptive_breaker.record_failure(error)
        elif self._breaker is not None:
            self._breaker._record_failure(error)

        if self._adaptive_retry is not None:
            self._adaptive_retry.record_outcome(attempt, False, 0.0)

    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate the retry delay for the given attempt."""
        if self._adaptive_retry is not None:
            return self._adaptive_retry.get_delay(attempt)
        if self._retry_config is not None:
            return calculate_delay(attempt, self._retry_config)
        return 0.0

    async def _execute_inner(
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Exception]:
        """Execute through breaker → retry → timeout → fn layers."""
        cb_err = self._evaluate_circuit_breaker()
        if cb_err is not None:
            return self._apply_fallback(cb_err)

        max_attempts = (
            self._retry_config.max_attempts if self._retry_config is not None else 1
        )
        return await self._execute_with_retries(max_attempts, fn, *args, **kwargs)

    async def _handle_retry_failure(
        self,
        error: Exception,
        attempt: int,
        max_attempts: int,
    ) -> bool:
        self._record_failure_outcome(error, attempt)
        if self._retry_config is not None and attempt < max_attempts:
            delay = self._calculate_retry_delay(attempt)
            await asyncio.sleep(min(delay, 3600.0))
            return True
        return False

    async def _execute_with_retries(
        self,
        max_attempts: int,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Exception]:
        last_error: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            result = await self._execute_with_timeout(fn, *args, **kwargs)
            match result:
                case Ok():
                    self._record_success_outcome(attempt)
                    return result
                case Err(error):
                    last_error = error
                    if await self._handle_retry_failure(error, attempt, max_attempts):
                        continue
                    break

        final_result: Result[T, Exception] = Err(
            last_error or RuntimeError("Execution failed")
        )
        return self._apply_fallback(final_result)

    async def _execute_with_timeout(
        self,
        fn: Callable[P, Awaitable[T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Exception]:
        """Execute fn with optional timeout.

        Args:
            fn: Async callable.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            ``Ok(result)`` or ``Err``.

        """
        try:
            if self._timeout is not None:
                result = await asyncio.wait_for(
                    fn(*args, **kwargs),
                    timeout=self._timeout,
                )
            else:
                result = await fn(*args, **kwargs)
            return Ok(result)
        except TimeoutError:
            return Err(
                TimeoutError(f"Pipeline '{self.name}' timed out after {self._timeout}s")
            )
        except Exception as exc:
            return Err(exc)

    def _apply_fallback(
        self,
        result: Result[T, Exception],
    ) -> Result[T, Exception]:
        """Apply fallback if configured and result is Err.

        Args:
            result: The result to potentially replace.

        Returns:
            Original result or ``Ok(fallback_value)``.

        """
        match result:
            case Err():
                if self._fallback_value is not _SENTINEL:
                    return Ok(cast(T, self._fallback_value))
            case Ok():
                pass
        return result


# Sentinel for distinguishing "no fallback" from "fallback=None"
_SENTINEL = object()
