import math

import pytest

from taipanstack.resilience.watchdogs._base import BaseWatcher


class DummyWatcher(BaseWatcher):
    async def _run(self) -> None:
        """Mocked method implementation."""


def test_watchdog_base_validation_negative_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        DummyWatcher(interval=-1.0)


def test_watchdog_base_validation_zero_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        DummyWatcher(interval=0.0)


def test_watchdog_base_validation_nan_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        DummyWatcher(interval=math.nan)


def test_watchdog_base_validation_inf_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        DummyWatcher(interval=math.inf)
