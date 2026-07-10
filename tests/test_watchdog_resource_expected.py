"""Tests for the ResourceWatcher and related utilities."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from taipanstack.core.result import Err, Ok
from taipanstack.resilience.watchdogs.resource_watcher import (
    ResourceSnapshot,
    ResourceWatcher,
    check_resources,
)


class TestResourceSnapshot:
    """Tests for the ResourceSnapshot dataclass."""

    def test_watchdog_resource_creation_expected(self) -> None:
        """Snapshot stores cpu, memory, and timestamp."""
        snap = ResourceSnapshot(cpu_percent=50.0, memory_percent=60.0, timestamp=1.0)
        assert snap.cpu_percent == 50.0
        assert snap.memory_percent == 60.0
        assert snap.timestamp == 1.0

    def test_watchdog_resource_frozen_expected(self) -> None:
        """Snapshot is immutable."""
        snap = ResourceSnapshot(cpu_percent=1.0, memory_percent=2.0, timestamp=0.0)
        with pytest.raises(AttributeError):
            snap.cpu_percent = 99.0  # type: ignore[misc]


class TestCheckResources:
    """Tests for the one-shot check_resources function."""

    def test_watchdog_resource_ok_with_psutil_expected(self) -> None:
        """Returns Ok(ResourceSnapshot) when psutil is available."""
        mock_vm = MagicMock()
        mock_vm.percent = 42.5
        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.return_value = 33.0
            mock_psutil.virtual_memory.return_value = mock_vm
            result = check_resources()

        assert isinstance(result, Ok)
        snap = result.ok_value
        assert snap.cpu_percent == 33.0
        assert snap.memory_percent == 42.5
        assert snap.timestamp > 0

    def test_watchdog_resource_err_without_psutil_expected(self) -> None:
        """Returns Err(ImportError) when psutil is not installed."""
        with patch(
            "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", False
        ):
            result = check_resources()

        assert isinstance(result, Err)
        assert isinstance(result.err_value, ImportError)


class TestResourceWatcher:
    """Tests for the ResourceWatcher background task."""

    @pytest.mark.asyncio
    async def test_watchdog_resource_start_without_psutil_returns_err_expected(
        self,
    ) -> None:
        """Start returns Err when psutil is unavailable."""
        watcher = ResourceWatcher()
        with patch(
            "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", False
        ):
            result = await watcher.start()
        assert isinstance(result, Err)
        assert isinstance(result.err_value, ImportError)

    @pytest.mark.asyncio
    async def test_watchdog_resource_start_stop_lifecycle_expected(
        self,
    ) -> None:
        """Watcher can be started and stopped."""
        mock_vm = MagicMock()
        mock_vm.percent = 10.0
        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.return_value = 5.0
            mock_psutil.virtual_memory.return_value = mock_vm

            watcher = ResourceWatcher(interval=0.05)
            result = await watcher.start()
            assert isinstance(result, Ok)
            assert watcher.is_running

            await asyncio.sleep(0.1)
            await watcher.stop()
            assert not watcher.is_running

    @pytest.mark.asyncio
    async def test_watchdog_resource_double_start_returns_err_expected(
        self,
    ) -> None:
        """Starting an already-running watcher returns Err."""
        mock_vm = MagicMock()
        mock_vm.percent = 10.0
        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.return_value = 5.0
            mock_psutil.virtual_memory.return_value = mock_vm

            watcher = ResourceWatcher(interval=0.05)
            await watcher.start()
            try:
                result = await watcher.start()
                assert isinstance(result, Err)
            finally:
                await watcher.stop()

    @pytest.mark.asyncio
    async def test_watchdog_resource_threshold_breach_callback_expected(
        self,
    ) -> None:
        """Callback fires when thresholds are breached."""
        breaches: list[tuple[str, float]] = []

        mock_vm = MagicMock()
        mock_vm.percent = 90.0
        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.return_value = 95.0
            mock_psutil.virtual_memory.return_value = mock_vm

            watcher = ResourceWatcher(
                interval=0.05,
                cpu_threshold=80.0,
                memory_threshold=80.0,
                on_threshold_breach=lambda r, v: breaches.append((r, v)),
            )
            await watcher.start()
            await asyncio.sleep(0.15)
            await watcher.stop()

        assert any(r == "cpu" for r, _ in breaches)
        assert any(r == "memory" for r, _ in breaches)

    @pytest.mark.asyncio
    async def test_watchdog_resource_no_breach_below_threshold_expected(
        self,
    ) -> None:
        """No callback when values are below thresholds."""
        breaches: list[tuple[str, float]] = []

        mock_vm = MagicMock()
        mock_vm.percent = 30.0
        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.return_value = 20.0
            mock_psutil.virtual_memory.return_value = mock_vm

            watcher = ResourceWatcher(
                interval=0.05,
                on_threshold_breach=lambda r, v: breaches.append((r, v)),
            )
            await watcher.start()
            await asyncio.sleep(0.15)
            await watcher.stop()

        assert len(breaches) == 0

    @pytest.mark.asyncio
    async def test_watchdog_resource_run_handles_check_error_expected(
        self,
    ) -> None:
        """Error from check_resources is logged, not raised."""
        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.side_effect = OSError("sensor fail")

            watcher = ResourceWatcher(interval=0.05)
            await watcher.start()
            await asyncio.sleep(0.15)
            await watcher.stop()
            # Should not crash — errors are caught by BaseWatcher._loop


class TestBaseWatcher:
    """Tests for BaseWatcher ABC."""

    def test_watchdog_resource_repr_expected(self) -> None:
        """Repr includes class name and interval."""
        watcher = ResourceWatcher(interval=3.0)
        assert "ResourceWatcher" in repr(watcher)
        assert "3.0" in repr(watcher)

    @pytest.mark.asyncio
    async def test_watchdog_resource_stop_without_start_expected(self) -> None:
        """Stopping a watcher that was never started is safe."""
        watcher = ResourceWatcher(interval=1.0)
        await watcher.stop()
        assert not watcher.is_running

    @pytest.mark.asyncio
    async def test_watchdog_resource_stop_timeout_cancels_task_expected(
        self,
    ) -> None:
        """When the task doesn't stop in time, it gets cancelled."""
        mock_vm = MagicMock()
        mock_vm.percent = 10.0

        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.return_value = 5.0
            mock_psutil.virtual_memory.return_value = mock_vm

            watcher = ResourceWatcher(interval=0.05)
            await watcher.start()

            # Force the task to hang by replacing it with a never-completing one
            original_task = watcher._task
            if original_task is not None:
                original_task.cancel()

            async def never_ends() -> None:
                await asyncio.sleep(9999)

            watcher._task = asyncio.create_task(never_ends())

            # stop() should timeout and cancel the task
            await watcher.stop()
            assert not watcher.is_running

    @pytest.mark.asyncio
    async def test_watchdog_resource_run_err_branch_logged_expected(
        self,
    ) -> None:
        """Err from check_resources in _run is handled gracefully."""
        with patch(
            "taipanstack.resilience.watchdogs.resource_watcher.check_resources"
        ) as mock_check:
            mock_check.return_value = Err(ImportError("no psutil"))

            watcher = ResourceWatcher(interval=0.05)
            # Call _run directly to hit the Err branch
            await watcher._run()

    @pytest.mark.asyncio
    async def test_watchdog_resource_threshold_breach_without_callback_expected(
        self,
    ) -> None:
        """Breach is logged but no crash when on_threshold_breach is None."""
        mock_vm = MagicMock()
        mock_vm.percent = 95.0
        with (
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher._HAS_PSUTIL", True
            ),
            patch(
                "taipanstack.resilience.watchdogs.resource_watcher.psutil"
            ) as mock_psutil,
        ):
            mock_psutil.cpu_percent.return_value = 99.0
            mock_psutil.virtual_memory.return_value = mock_vm

            # No callback set — on_threshold_breach=None
            watcher = ResourceWatcher(
                interval=0.05,
                cpu_threshold=80.0,
                memory_threshold=80.0,
            )
            await watcher.start()
            await asyncio.sleep(0.1)
            await watcher.stop()


@pytest.mark.asyncio
async def test_watchdog_resource_resource_watcher_run_err_branch_expected_expected() -> (
    None
):
    from unittest.mock import patch

    from taipanstack.core.result import Err
    from taipanstack.resilience.watchdogs.resource_watcher import ResourceWatcher

    watcher = ResourceWatcher(interval=0.1)

    with patch(
        "taipanstack.resilience.watchdogs.resource_watcher.check_resources",
        return_value=Err(RuntimeError("mock_err")),
    ):
        # Calls the watcher's loop manually once to hit the `Err` branch
        await watcher._run()


def test_watchdog_resource_resource_watcher_import_error_coverage_expected() -> (
    None
):
    """Test resource_watcher import error fallback branches."""
    import asyncio
    import importlib
    import sys

    from taipanstack.core.result import Err

    original_psutil = sys.modules.pop("psutil", None)
    sys.modules["psutil"] = None  # type: ignore
    try:
        import taipanstack.resilience.watchdogs.resource_watcher as res_mod

        importlib.reload(res_mod)
        assert res_mod._HAS_PSUTIL is False

        # Test the start error branch where psutil is not available
        watcher = res_mod.ResourceWatcher()

        async def test_watchdog_resource_run_ok_expected():
            result = await watcher.start()
            assert isinstance(result, Err)
            # To test the unhandled _run case, we manually toggle _is_running
            watcher._is_running = True
            await watcher._run()

            # Test check_resources directly
            res = res_mod.check_resources()
            assert isinstance(res, Err)

        asyncio.run(test_watchdog_resource_run_ok_expected())
    finally:
        if original_psutil is not None:
            sys.modules["psutil"] = original_psutil
        else:
            sys.modules.pop("psutil", None)
        importlib.reload(res_mod)


def test_watchdog_resource_resource_watcher_import_success_coverage_expected() -> (
    None
):
    """Test resource_watcher import success branch."""
    import importlib
    import sys
    import types

    # Create a mock module for psutil
    mock_psutil = types.ModuleType("psutil")

    original_psutil = sys.modules.pop("psutil", None)
    sys.modules["psutil"] = mock_psutil
    try:
        import taipanstack.resilience.watchdogs.resource_watcher as res_mod

        importlib.reload(res_mod)
        assert res_mod._HAS_PSUTIL is True
    finally:
        if original_psutil is not None:
            sys.modules["psutil"] = original_psutil
        else:
            sys.modules.pop("psutil", None)
        importlib.reload(res_mod)
