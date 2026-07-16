"""
Health pinger — proactively checks dependency health.

Runs async health checks against registered targets. If a target
becomes unhealthy the associated ``CircuitBreaker`` is opened
preventively.
"""

import asyncio
import logging
import math
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState
from taipanstack.resilience.watchdogs._base import BaseWatcher

logger = logging.getLogger("taipanstack.resilience.watchdogs.health")


@dataclass
class HealthTarget:
    """A dependency to be monitored by :class:`HealthPinger`.

    Attributes:
        name: Human-readable name for logging.
        check: Async callable returning ``True`` if the target is
            healthy, ``False`` otherwise.
        circuit_breaker: Optional circuit breaker to open on failure.

    """

    name: str
    check: Callable[[], Awaitable[bool]]
    circuit_breaker: CircuitBreaker | None = None


async def check_target(target: HealthTarget) -> Result[bool, Exception]:
    """Run a single health check.

    Args:
        target: The target to check.

    Returns:
        ``Ok(True)`` if healthy, ``Ok(False)`` if unhealthy,
        ``Err`` if the check itself raises.

    """
    try:
        healthy = await target.check()
        return Ok(healthy)
    except Exception as exc:
        return Err(exc)


async def check_all(
    targets: Sequence[HealthTarget],
) -> Result[dict[str, bool], Exception]:
    """Run health checks for all targets concurrently.

    Args:
        targets: Targets to check.

    Returns:
        ``Ok(dict)`` mapping target names to health status.

    """
    # Run all checks concurrently
    check_results = await asyncio.gather(*(check_target(t) for t in targets))

    results: dict[str, bool] = {}
    for target, result in zip(targets, check_results, strict=True):
        if isinstance(result, Ok):
            results[target.name] = result.ok_value
        else:
            logger.warning(
                "Health check for '%s' failed during aggregation: %s",
                target.name,
                result.err_value,
            )
            results[target.name] = False
    return Ok(results)


class HealthPinger(BaseWatcher):
    """Background watcher that pings external dependencies.

    For each registered ``HealthTarget``, calls its ``check``
    coroutine on every cycle. If a target is unhealthy and has
    an associated ``CircuitBreaker``, the breaker is opened
    preventively.

    Args:
        targets: Dependencies to monitor.
        interval: Seconds between ping cycles.
        on_health_change: Optional callback ``(name, is_healthy)``.

    Example:
        >>> async def db_ping() -> bool:
        ...     return await pool.fetchval("SELECT 1") == 1
        >>> pinger = HealthPinger(
        ...     targets=[HealthTarget("db", db_ping, breaker)],
        ... )
        >>> await pinger.start()

    """

    def __init__(
        self,
        *,
        targets: Sequence[HealthTarget],
        interval: float = 10.0,
        on_health_change: Callable[[str, bool], None] | None = None,
    ) -> None:
        """Initialize the health pinger.

        Args:
            targets: Dependencies to monitor.
            interval: Seconds between ping cycles.
            on_health_change: Optional callback on status change.

        """
        if not math.isfinite(interval) or interval <= 0:
            raise ValueError("interval must be a finite positive number")
        super().__init__(interval=interval)
        self._targets = list(targets)
        self._on_health_change = on_health_change
        self._last_status: dict[str, bool] = {}

    async def _process_target(self, target: HealthTarget) -> None:
        """Process a single health target."""
        result = await check_target(target)

        if isinstance(result, Ok):
            is_healthy = result.ok_value
        else:
            logger.warning(
                "Health check for '%s' raised: %s",
                target.name,
                result.err_value,
            )
            is_healthy = False

        self._update_target_status(target, is_healthy)

    def _check_and_open_breaker(self, target: HealthTarget, is_healthy: bool) -> None:
        """Open circuit breaker preventively on failure (always checked)."""
        if (
            not is_healthy
            and target.circuit_breaker is not None
            and target.circuit_breaker.state != CircuitState.OPEN
        ):
            _force_open_breaker(target.circuit_breaker, target.name)

    def _notify_health_change(self, target: HealthTarget, is_healthy: bool) -> None:
        """Notify on health status change and log it."""
        if self._on_health_change is not None:
            self._on_health_change(target.name, is_healthy)

        if is_healthy:
            logger.info("Target '%s' is now healthy", target.name)
        else:
            logger.warning("Target '%s' is now unhealthy", target.name)

    def _update_target_status(self, target: HealthTarget, is_healthy: bool) -> None:
        """Update target status and handle side-effects."""
        previous = self._last_status.get(target.name)

        self._check_and_open_breaker(target, is_healthy)

        if previous == is_healthy:
            return

        self._last_status[target.name] = is_healthy

        self._notify_health_change(target, is_healthy)

    async def _run(self) -> None:
        """Execute a single health-check cycle concurrently."""
        await asyncio.gather(*(self._process_target(t) for t in self._targets))


def _force_open_breaker(breaker: CircuitBreaker, target_name: str) -> None:
    """Force a circuit breaker into OPEN state.

    Simulates enough failures to trip the breaker by recording
    a synthetic exception.

    Args:
        breaker: The circuit breaker to trip.
        target_name: Target name for logging context.

    """
    synthetic = ConnectionError(f"Health ping failed for '{target_name}'")

    # Record failures until the breaker opens, but cap it to avoid infinite loops
    # if the circuit breaker's state is corrupted or mutated.
    max_attempts = breaker.config.failure_threshold + 5
    attempts = 0

    while breaker.state != CircuitState.OPEN and attempts < max_attempts:
        breaker._record_failure(synthetic)
        attempts += 1

    if breaker.state != CircuitState.OPEN:
        # Force open if it didn't open normally
        old_state = breaker.state
        with breaker._state.lock:
            breaker._state.state = CircuitState.OPEN
        breaker._notify_state_change(old_state, CircuitState.OPEN)

    logger.warning(
        "Circuit breaker '%s' opened preventively for target '%s'",
        breaker.name,
        target_name,
    )
