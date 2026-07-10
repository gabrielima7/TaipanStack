import asyncio
from unittest.mock import patch

import pytest

from taipanstack.resilience.watchdogs._base import BaseWatcher


class DummyWatcher(BaseWatcher):
    async def _run(self) -> None:
        await asyncio.sleep(0.01)


@pytest.mark.asyncio
async def test_chaos_watchdogs_base_watcher_stop_timeout_error_expected() -> (
    None
):
    """Test that BaseWatcher.stop gracefully handles TimeoutError."""
    watcher = DummyWatcher(interval=0.1)
    await watcher.start()

    await asyncio.sleep(0.05)

    async def side_effect(aw, timeout=None):
        aw.cancel()
        raise TimeoutError("Simulated timeout")

    with patch("asyncio.wait_for", side_effect=side_effect):
        await watcher.stop()

    assert not watcher.is_running


@pytest.mark.asyncio
async def test_chaos_watchdogs_base_watcher_stop_oserror_expected() -> None:
    """Test that BaseWatcher.stop propagates unhandled exceptions like OSError."""
    watcher = DummyWatcher(interval=0.1)
    await watcher.start()

    await asyncio.sleep(0.05)

    async def side_effect(aw, timeout=None):
        aw.cancel()
        raise OSError("Resource exhaustion")

    with patch("asyncio.wait_for", side_effect=side_effect):
        with pytest.raises(OSError, match="Resource exhaustion"):
            await watcher.stop()


@pytest.mark.asyncio
async def test_chaos_watchdogs_base_watcher_loop_timeout_error_expected() -> (
    None
):
    """Test that BaseWatcher._loop catches TimeoutError from stop_event.wait."""
    watcher = DummyWatcher(interval=0.1)

    call_count = 0

    async def side_effect_wait_for(aw, timeout=None):
        nonlocal call_count
        aw.close()
        call_count += 1
        if call_count == 1:
            raise TimeoutError("Simulated timeout in loop")
        # Second time let it stop to avoid infinite loop
        watcher._stop_event.set()

    await watcher.start()

    await asyncio.sleep(0.05)

    with patch("asyncio.wait_for", side_effect=side_effect_wait_for):
        # We need to wait for the loop to run and hit our mocked wait_for
        await asyncio.sleep(0.2)

    await watcher.stop()


@pytest.mark.asyncio
async def test_chaos_watchdogs_base_watcher_start_stop_event_clear_expected() -> (
    None
):
    watcher = DummyWatcher(interval=0.1)
    await watcher.start()
    await watcher.stop()
    assert watcher._stop_event.is_set()
    await watcher.start()
    assert not watcher._stop_event.is_set()
    await watcher.stop()
