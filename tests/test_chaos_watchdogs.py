import asyncio
from unittest.mock import patch

import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState
from taipanstack.resilience.watchdogs._base import BaseWatcher
from taipanstack.resilience.watchdogs.health_pinger import HealthPinger, HealthTarget


class DummyWatcher(BaseWatcher):
    async def _run(self) -> None:
        await asyncio.sleep(0.01)


@pytest.mark.asyncio
async def test_chaos_watchdogs_base_watcher_stop_cancelled_error() -> None:
    """Test that BaseWatcher.stop gracefully handles asyncio.CancelledError."""
    watcher = DummyWatcher(interval=0.1)
    await watcher.start()

    # Wait for task to spin up
    await asyncio.sleep(0.05)

    with patch("asyncio.wait_for", side_effect=asyncio.CancelledError):
        await watcher.stop()

    # The task should be cancelled and not running
    assert not watcher.is_running


@pytest.mark.asyncio
async def test_chaos_watchdogs_base_watcher_loop_exception_handling() -> None:
    """Test that BaseWatcher._loop catches Exceptions from _run without crashing the loop."""
    watcher = DummyWatcher(interval=0.1)

    call_count = 0

    async def failing_run() -> None:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RuntimeError("Chaos loop failure")
        elif call_count == 2:
            await asyncio.sleep(0.01)  # Recover on second call

    watcher._run = failing_run  # type: ignore

    await watcher.start()

    # Wait enough time for two cycles to pass
    # Using 0.25 avoids sleep dependency by having a predictable loop
    await asyncio.sleep(0.25)

    await watcher.stop()

    # Ensure it survived the crash and ran again
    assert call_count >= 2


@pytest.mark.asyncio
async def test_chaos_watchdogs_health_pinger_skips_open_breaker() -> None:
    """Test that _check_and_open_breaker skips if breaker is already OPEN."""
    breaker = CircuitBreaker(name="test_breaker", failure_threshold=5)
    breaker._state.state = CircuitState.OPEN

    # We use a mock check to ensure the target is "unhealthy"
    async def always_unhealthy() -> bool:
        return False

    target = HealthTarget(
        name="test_target", check=always_unhealthy, circuit_breaker=breaker
    )

    pinger = HealthPinger(targets=[target], interval=0.1)

    # We call _update_target_status directly since this is what triggers _check_and_open_breaker
    with patch(
        "taipanstack.resilience.watchdogs.health_pinger._force_open_breaker"
    ) as mock_force:
        pinger._update_target_status(target, is_healthy=False)

        # Should not be called because breaker is already OPEN
        mock_force.assert_not_called()
