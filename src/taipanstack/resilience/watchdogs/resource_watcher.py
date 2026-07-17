"""
Resource watcher — monitors CPU and memory usage.

When usage breaches configurable thresholds, invokes a callback
so the application can react (e.g. tighten rate limits).
"""

import logging
import math
import time
from collections.abc import Callable
from dataclasses import dataclass

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.watchdogs._base import BaseWatcher

logger = logging.getLogger("taipanstack.resilience.watchdogs.resource")

try:
    import psutil

    _HAS_PSUTIL = True
except ImportError:
    psutil = None
    _HAS_PSUTIL = False


@dataclass(frozen=True)
class ResourceSnapshot:
    """Point-in-time snapshot of system resource usage.

    Attributes:
        cpu_percent: Current CPU utilisation (0-100).
        memory_percent: Current memory utilisation (0-100).
        timestamp: Monotonic timestamp of the reading.

    """

    cpu_percent: float
    memory_percent: float
    timestamp: float


def _validate_interval(interval: float) -> None:
    """Validate interval parameter."""
    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("interval must be a finite positive number")


def _validate_threshold(name: str, value: float) -> None:
    """Validate a threshold parameter."""
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite non-negative number")


def check_resources() -> Result[ResourceSnapshot, Exception]:
    """Take a one-shot resource reading.

    Returns:
        ``Ok(ResourceSnapshot)`` on success, ``Err`` if psutil is
        unavailable.

    """
    if not _HAS_PSUTIL:
        return Err(
            ImportError(
                "psutil is required for resource monitoring. "
                "Install with: pip install taipanstack[resilience]",
            ),
        )

    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent
    return Ok(
        ResourceSnapshot(
            cpu_percent=cpu,
            memory_percent=mem,
            timestamp=time.monotonic(),
        ),
    )


class ResourceWatcher(BaseWatcher):
    """Background watcher that monitors CPU and memory.

    When either metric exceeds its configured threshold the
    ``on_threshold_breach`` callback is invoked with the resource
    name (``"cpu"`` or ``"memory"``) and the current value.

    Args:
        interval: Seconds between checks.
        cpu_threshold: CPU percentage that triggers a breach.
        memory_threshold: Memory percentage that triggers a breach.
        on_threshold_breach: Optional callback ``(resource, value) -> None``.

    Example:
        >>> watcher = ResourceWatcher(
        ...     cpu_threshold=80.0,
        ...     on_threshold_breach=lambda r, v: print(f"{r} at {v}%"),
        ... )
        >>> await watcher.start()

    """

    def __init__(
        self,
        *,
        interval: float = 5.0,
        cpu_threshold: float = 85.0,
        memory_threshold: float = 85.0,
        on_threshold_breach: Callable[[str, float], None] | None = None,
    ) -> None:
        """Initialize the resource watcher.

        Args:
            interval: Seconds between checks.
            cpu_threshold: CPU percentage that triggers a breach.
            memory_threshold: Memory percentage that triggers a breach.
            on_threshold_breach: Optional breach callback.

        """
        _validate_interval(interval)
        _validate_threshold("cpu_threshold", cpu_threshold)
        _validate_threshold("memory_threshold", memory_threshold)

        super().__init__(interval=interval)
        self._cpu_threshold = cpu_threshold
        self._memory_threshold = memory_threshold
        self._on_threshold_breach = on_threshold_breach

    async def start(self) -> Result[None, Exception]:
        """Start the resource watcher.

        Returns:
            ``Err`` if psutil is not installed, otherwise delegates
            to ``BaseWatcher.start()``.

        """
        if not _HAS_PSUTIL:
            return Err(
                ImportError(
                    "psutil is required for ResourceWatcher. "
                    "Install with: pip install taipanstack[resilience]",
                ),
            )
        return await super().start()

    def _check_threshold(self, name: str, value: float, threshold: float) -> None:
        if value >= threshold:
            logger.warning(
                "%s threshold breached: %.1f%% >= %.1f%%",
                name.capitalize(),
                value,
                threshold,
            )
            if self._on_threshold_breach is not None:
                self._on_threshold_breach(name, value)

    def _handle_snapshot(self, snapshot: ResourceSnapshot) -> None:
        self._check_threshold("cpu", snapshot.cpu_percent, self._cpu_threshold)
        self._check_threshold("memory", snapshot.memory_percent, self._memory_threshold)

    async def _run(self) -> None:
        """Execute a single resource check cycle."""
        result = check_resources()
        if isinstance(result, Ok):
            self._handle_snapshot(result.ok_value)
        else:
            logger.error("Resource check failed: %s", result.err_value)
