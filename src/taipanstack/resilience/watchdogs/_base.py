"""
Base watcher abstract class.

Provides a shared lifecycle (start/stop) for all background
watchdog tasks running on the asyncio event loop.
"""

import asyncio
import logging
from abc import ABC, abstractmethod

from taipanstack.core.result import Err, Ok, Result

logger = logging.getLogger("taipanstack.resilience.watchdogs")


class BaseWatcher(ABC):
    """Abstract base for background watchdog tasks.

    Subclasses implement ``_run`` which is called repeatedly at
    ``_interval`` seconds until ``stop`` is called.

    Args:
        interval: Seconds between each poll cycle.

    Example:
        >>> class MyWatcher(BaseWatcher):
        ...     async def _run(self) -> None:
        ...         print("checking...")
        >>> watcher = MyWatcher(interval=5.0)
        >>> await watcher.start()

    """

    def __init__(self, *, interval: float = 5.0) -> None:
        """Initialize the base watcher.

        Args:
            interval: Seconds between each poll cycle.

        """
        self._interval = interval
        self._stop_event: asyncio.Event = asyncio.Event()
        self._task: asyncio.Task[None] | None = None

    @property
    def is_running(self) -> bool:
        """Return ``True`` if the background task is active."""
        return self._task is not None and not self._task.done()

    async def start(self) -> Result[None, Exception]:
        """Start the background watcher loop.

        Returns:
            ``Ok(None)`` on success, ``Err`` if already running.

        """
        if self.is_running:
            return Err(RuntimeError("Watcher is already running"))

        self._stop_event.clear()
        self._task = asyncio.create_task(self._loop())
        logger.info("%s started (interval=%.1fs)", type(self).__name__, self._interval)
        return Ok(None)

    async def stop(self) -> None:
        """Signal the watcher to stop and wait for it to finish."""
        self._stop_event.set()
        if self._task is not None:
            try:
                await asyncio.wait_for(self._task, timeout=self._interval + 1.0)
            except (TimeoutError, asyncio.CancelledError):
                self._task.cancel()
            self._task = None
        logger.info("%s stopped", type(self).__name__)

    async def _loop(self) -> None:
        """Internal loop that calls ``_run`` at each interval."""
        while not self._stop_event.is_set():
            try:
                await self._run()
            except Exception:
                logger.exception("%s encountered an error", type(self).__name__)
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self._interval)
            except TimeoutError:
                continue

    @abstractmethod
    async def _run(self) -> None:
        """Execute a single poll cycle.

        Subclasses must override this with the actual monitoring logic.
        """
        ...

    def _get_extra_repr(self) -> dict[str, object]:
        """Return extra fields for ``__repr__``.

        Subclasses can override to add custom fields.
        """
        return {}

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        extras = self._get_extra_repr()
        parts = [f"interval={self._interval}"]
        parts.extend(f"{k}={v}" for k, v in extras.items())
        return f"{type(self).__name__}({', '.join(parts)})"
