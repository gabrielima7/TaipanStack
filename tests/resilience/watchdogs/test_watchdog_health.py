"""Tests for the HealthPinger and related utilities."""

import asyncio

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState
from taipanstack.resilience.watchdogs.health_pinger import (
    HealthPinger,
    HealthTarget,
    _force_open_breaker,
    check_all,
    check_target,
)

# --- helpers -----------------------------------------------------------------


async def _healthy() -> bool:
    return True


async def _unhealthy() -> bool:
    return False


async def _exploding() -> bool:
    raise ConnectionError("boom")


# --- check_target ------------------------------------------------------------


class TestCheckTarget:
    """Tests for the one-shot check_target function."""

    @pytest.mark.asyncio
    async def test_healthy_target(self) -> None:
        """Returns Ok(True) for a healthy target."""
        target = HealthTarget(name="db", check=_healthy)
        result = await check_target(target)
        assert isinstance(result, Ok)
        assert result.ok_value is True

    @pytest.mark.asyncio
    async def test_unhealthy_target(self) -> None:
        """Returns Ok(False) for an unhealthy target."""
        target = HealthTarget(name="db", check=_unhealthy)
        result = await check_target(target)
        assert isinstance(result, Ok)
        assert result.ok_value is False

    @pytest.mark.asyncio
    async def test_exploding_target(self) -> None:
        """Returns Err when the check raises."""
        target = HealthTarget(name="db", check=_exploding)
        result = await check_target(target)
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ConnectionError)


# --- check_all ---------------------------------------------------------------


class TestCheckAll:
    """Tests for check_all function."""

    @pytest.mark.asyncio
    async def test_all_healthy(self) -> None:
        """All targets healthy."""
        targets = [
            HealthTarget(name="db", check=_healthy),
            HealthTarget(name="cache", check=_healthy),
        ]
        result = await check_all(targets)
        assert isinstance(result, Ok)
        assert result.ok_value == {"db": True, "cache": True}

    @pytest.mark.asyncio
    async def test_mixed_health(self) -> None:
        """Mix of healthy and unhealthy."""
        targets = [
            HealthTarget(name="db", check=_healthy),
            HealthTarget(name="cache", check=_unhealthy),
        ]
        result = await check_all(targets)
        assert isinstance(result, Ok)
        assert result.ok_value["db"] is True
        assert result.ok_value["cache"] is False

    @pytest.mark.asyncio
    async def test_exploding_counted_as_unhealthy(self) -> None:
        """An exception from check is treated as unhealthy."""
        targets = [HealthTarget(name="svc", check=_exploding)]
        result = await check_all(targets)
        assert isinstance(result, Ok)
        assert result.ok_value["svc"] is False


# --- _force_open_breaker ------------------------------------------------------


class TestForceOpenBreaker:
    """Tests for _force_open_breaker helper."""

    def test_opens_closed_breaker(self) -> None:
        """Force-opens a CLOSED circuit breaker."""
        breaker = CircuitBreaker(name="test", failure_threshold=3)
        assert breaker.state == CircuitState.CLOSED

        _force_open_breaker(breaker, "db")
        assert breaker.state.value == CircuitState.OPEN.value


# --- HealthPinger -------------------------------------------------------------


class TestHealthPinger:
    """Tests for the HealthPinger background task."""

    @pytest.mark.asyncio
    async def test_start_stop_lifecycle(self) -> None:
        """Pinger can be started and stopped."""
        pinger = HealthPinger(
            targets=[HealthTarget(name="db", check=_healthy)],
            interval=0.05,
        )
        result = await pinger.start()
        assert isinstance(result, Ok)
        assert pinger.is_running

        await asyncio.sleep(0.1)
        await pinger.stop()
        assert not pinger.is_running

    @pytest.mark.asyncio
    async def test_health_change_callback(self) -> None:
        """Callback fires on status transitions."""
        changes: list[tuple[str, bool]] = []

        call_count = 0

        async def flaky() -> bool:
            nonlocal call_count
            call_count += 1
            return call_count > 2

        pinger = HealthPinger(
            targets=[HealthTarget(name="svc", check=flaky)],
            interval=0.05,
            on_health_change=lambda n, h: changes.append((n, h)),
        )
        await pinger.start()
        await asyncio.sleep(0.3)
        await pinger.stop()

        # Should have at least an unhealthy then healthy transition
        names = [c[0] for c in changes]
        assert "svc" in names

    @pytest.mark.asyncio
    async def test_opens_breaker_on_failure(self) -> None:
        """Circuit breaker is opened when target is unhealthy."""
        breaker = CircuitBreaker(name="db_breaker", failure_threshold=2)

        pinger = HealthPinger(
            targets=[
                HealthTarget(name="db", check=_unhealthy, circuit_breaker=breaker),
            ],
            interval=0.05,
        )
        await pinger.start()
        await asyncio.sleep(0.15)
        await pinger.stop()

        assert breaker.state.value == CircuitState.OPEN.value

    @pytest.mark.asyncio
    async def test_does_not_close_breaker_on_recovery(self) -> None:
        """Recovery does NOT force-close the circuit breaker.

        Natural recovery (half-open → closed) is handled by CircuitBreaker itself.
        """
        breaker = CircuitBreaker(name="db_breaker", failure_threshold=1, timeout=999.0)

        call_count = 0

        async def recovering() -> bool:
            nonlocal call_count
            call_count += 1
            return call_count > 2

        pinger = HealthPinger(
            targets=[
                HealthTarget(name="db", check=recovering, circuit_breaker=breaker),
            ],
            interval=0.05,
        )
        await pinger.start()
        await asyncio.sleep(0.3)
        await pinger.stop()

        # Breaker was opened and stays open (timeout=999s so no half-open)
        assert breaker.state.value == CircuitState.OPEN.value

    @pytest.mark.asyncio
    async def test_exception_in_check_treated_as_unhealthy(self) -> None:
        """An exception from the check coroutine is treated as unhealthy."""
        changes: list[tuple[str, bool]] = []

        pinger = HealthPinger(
            targets=[HealthTarget(name="svc", check=_exploding)],
            interval=0.05,
            on_health_change=lambda n, h: changes.append((n, h)),
        )
        await pinger.start()
        await asyncio.sleep(0.15)
        await pinger.stop()

        assert any(h is False for _, h in changes)

    @pytest.mark.asyncio
    async def test_no_duplicate_callback_on_same_status(self) -> None:
        """Callback only fires on *transitions*, not every cycle."""
        changes: list[tuple[str, bool]] = []

        pinger = HealthPinger(
            targets=[HealthTarget(name="stable", check=_healthy)],
            interval=0.05,
            on_health_change=lambda n, h: changes.append((n, h)),
        )
        await pinger.start()
        await asyncio.sleep(0.25)
        await pinger.stop()

        # Only one transition: None -> True
        assert len(changes) == 1
        assert changes[0] == ("stable", True)
