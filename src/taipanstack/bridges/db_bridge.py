"""
DB Bridge — resilient database wrappers.

Wraps SQLAlchemy async engine and Redis async client with
TaipanStack's circuit breaker and retry patterns.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)
from taipanstack.resilience.retry import RetryConfig, calculate_delay

logger = logging.getLogger("taipanstack.bridges.db")

# --- optional imports ------------------------------------------------------

try:
    import sqlalchemy  # noqa: F401
    from sqlalchemy import text as sa_text  # pragma: no cover
    from sqlalchemy.ext.asyncio import AsyncSession  # pragma: no cover

    _HAS_SQLALCHEMY = True  # pragma: no cover
except ImportError:  # pragma: no cover
    _HAS_SQLALCHEMY = False

try:
    import redis.asyncio as aioredis

    _HAS_REDIS = True  # pragma: no cover
except ImportError:  # pragma: no cover
    _HAS_REDIS = False

if TYPE_CHECKING:
    import redis.asyncio as aioredis
    from sqlalchemy.ext.asyncio import AsyncEngine


def _breaker_is_open(cb: CircuitBreaker) -> CircuitBreakerError | None:
    """Return a ``CircuitBreakerError`` if the breaker is OPEN.

    Args:
        cb: The circuit breaker to check.

    Returns:
        Error if open, ``None`` otherwise.

    """
    if cb.state == CircuitState.OPEN:
        return CircuitBreakerError(
            f"Circuit breaker '{cb.name}' is OPEN",
            state=cb.state,
        )
    return None


class ResilientDatabase:
    """Wraps a SQLAlchemy async engine with resilience patterns.

    Args:
        engine: SQLAlchemy ``AsyncEngine`` instance.
        circuit_breaker: Optional circuit breaker.
        retry_config: Optional retry configuration.

    Example:
        >>> db = ResilientDatabase(engine, circuit_breaker=breaker)
        >>> result = await db.execute(text("SELECT 1"))

    """

    def __init__(
        self,
        engine: AsyncEngine,
        *,
        circuit_breaker: CircuitBreaker | None = None,
        retry_config: RetryConfig | None = None,
    ) -> None:
        """Initialize the resilient database wrapper.

        Args:
            engine: SQLAlchemy AsyncEngine.
            circuit_breaker: Optional circuit breaker.
            retry_config: Optional retry config.

        """
        self._engine = engine
        self._circuit_breaker = circuit_breaker
        self._retry_config = retry_config

    async def _execute_loop(
        self,
        statement: object,
        max_attempts: int,
        **kwargs: object,
    ) -> Result[object, Exception]:
        """Execute the retry loop for database operations."""
        last_error: Exception | None = None

        for attempt in range(1, max_attempts + 1):
            try:
                async with AsyncSession(self._engine) as session:
                    result = await session.execute(statement, **kwargs)
                    return Ok(result)
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "DB execute attempt %d failed: %s",
                    attempt,
                    exc,
                )
                if self._circuit_breaker is not None:
                    self._circuit_breaker._record_failure(exc)
                if self._retry_config is not None and attempt < max_attempts:
                    delay = calculate_delay(attempt, self._retry_config)
                    await asyncio.sleep(delay)
                    continue
                break

        return Err(last_error or RuntimeError("Database execute failed"))

    async def execute(
        self,
        statement: object,
        **kwargs: object,
    ) -> Result[object, Exception]:
        """Execute a SQL statement with resilience.

        Args:
            statement: SQLAlchemy statement to execute.
            **kwargs: Passed to ``session.execute``.

        Returns:
            ``Ok(result)`` on success, ``Err`` on failure.

        """
        if not _HAS_SQLALCHEMY:
            return Err(
                ImportError(
                    "sqlalchemy is required for ResilientDatabase. "
                    "Install with: pip install taipanstack[bridges-db]"
                )
            )

        # Circuit breaker gate
        if self._circuit_breaker is not None:
            cb_err = _breaker_is_open(self._circuit_breaker)
            if cb_err is not None:
                return Err(cb_err)

        max_attempts = 1
        if self._retry_config is not None:
            max_attempts = self._retry_config.max_attempts

        return await self._execute_loop(statement, max_attempts, **kwargs)

    async def health_check(self) -> Result[bool, Exception]:
        """Check database connectivity.

        Executes ``SELECT 1`` to verify the connection is alive.

        Returns:
            ``Ok(True)`` if healthy, ``Err`` on failure.

        """
        if not _HAS_SQLALCHEMY:
            return Err(ImportError("sqlalchemy is required for health check"))

        try:
            async with AsyncSession(self._engine) as session:
                await session.execute(sa_text("SELECT 1"))
                return Ok(True)
        except Exception as exc:
            return Err(exc)


class ResilientRedis:
    """Wraps a Redis async client with resilience patterns.

    Args:
        client: ``redis.asyncio.Redis`` instance.
        circuit_breaker: Optional circuit breaker.

    Example:
        >>> r = ResilientRedis(redis_client, circuit_breaker=breaker)
        >>> result = await r.execute("GET", "my_key")

    """

    def __init__(
        self,
        client: aioredis.Redis[bytes | str],
        *,
        circuit_breaker: CircuitBreaker | None = None,
    ) -> None:
        """Initialize the resilient Redis wrapper.

        Args:
            client: Redis async client.
            circuit_breaker: Optional circuit breaker.

        """
        self._client = client
        self._circuit_breaker = circuit_breaker

    async def execute(
        self,
        command: str,
        *args: object,
    ) -> Result[object, Exception]:
        """Execute a Redis command with resilience.

        Args:
            command: Redis command name (e.g. ``"GET"``, ``"SET"``).
            *args: Command arguments.

        Returns:
            ``Ok(result)`` on success, ``Err`` on failure.

        """
        if not _HAS_REDIS:
            return Err(
                ImportError(
                    "redis is required for ResilientRedis. "
                    "Install with: pip install taipanstack[bridges-db]"
                )
            )

        # Circuit breaker gate
        if self._circuit_breaker is not None:
            cb_err = _breaker_is_open(self._circuit_breaker)
            if cb_err is not None:
                return Err(cb_err)

        try:
            fn = getattr(self._client, command.lower())
            result = await fn(*args)
            return Ok(result)
        except Exception as exc:
            logger.warning("Redis command '%s' failed: %s", command, exc)
            if self._circuit_breaker is not None:
                self._circuit_breaker._record_failure(exc)
            return Err(exc)

    async def health_check(self) -> Result[bool, Exception]:
        """Check Redis connectivity via PING.

        Returns:
            ``Ok(True)`` if healthy, ``Err`` on failure.

        """
        if not _HAS_REDIS:
            return Err(ImportError("redis is required for health check"))

        try:
            pong = await self._client.ping()
            return Ok(bool(pong))
        except Exception as exc:
            return Err(exc)
