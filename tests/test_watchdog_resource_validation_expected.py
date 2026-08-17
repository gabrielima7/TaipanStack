import math

import pytest

from taipanstack.resilience.watchdogs.resource_watcher import ResourceWatcher


def test_watchdog_resource_validation_negative_interval_expected():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=-1.0)


def test_watchdog_resource_validation_zero_interval_expected():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=0.0)


def test_watchdog_resource_validation_nan_interval_expected():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=math.nan)


def test_watchdog_resource_validation_inf_interval_expected():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=math.inf)


def test_watchdog_resource_validation_negative_cpu_expected():
    with pytest.raises(
        ValueError, match="cpu_threshold must be a finite non-negative number"
    ):
        ResourceWatcher(cpu_threshold=-1.0)


def test_watchdog_resource_validation_nan_cpu_expected():
    with pytest.raises(
        ValueError, match="cpu_threshold must be a finite non-negative number"
    ):
        ResourceWatcher(cpu_threshold=math.nan)


def test_watchdog_resource_validation_inf_cpu_expected():
    with pytest.raises(
        ValueError, match="cpu_threshold must be a finite non-negative number"
    ):
        ResourceWatcher(cpu_threshold=math.inf)


def test_watchdog_resource_validation_negative_memory_expected():
    with pytest.raises(
        ValueError, match="memory_threshold must be a finite non-negative number"
    ):
        ResourceWatcher(memory_threshold=-1.0)


def test_watchdog_resource_validation_nan_memory_expected():
    with pytest.raises(
        ValueError, match="memory_threshold must be a finite non-negative number"
    ):
        ResourceWatcher(memory_threshold=math.nan)


def test_watchdog_resource_validation_inf_memory_expected():
    with pytest.raises(
        ValueError, match="memory_threshold must be a finite non-negative number"
    ):
        ResourceWatcher(memory_threshold=math.inf)
