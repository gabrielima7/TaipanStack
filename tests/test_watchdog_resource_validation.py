import math

import pytest

from taipanstack.resilience.watchdogs.resource_watcher import ResourceWatcher


def test_watchdog_resource_validation_negative_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=-1.0)

def test_watchdog_resource_validation_zero_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=0.0)

def test_watchdog_resource_validation_nan_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=math.nan)

def test_watchdog_resource_validation_inf_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ResourceWatcher(interval=math.inf)

def test_watchdog_resource_validation_negative_cpu():
    with pytest.raises(ValueError, match="cpu_threshold must be a finite non-negative number"):
        ResourceWatcher(cpu_threshold=-1.0)

def test_watchdog_resource_validation_nan_cpu():
    with pytest.raises(ValueError, match="cpu_threshold must be a finite non-negative number"):
        ResourceWatcher(cpu_threshold=math.nan)

def test_watchdog_resource_validation_inf_cpu():
    with pytest.raises(ValueError, match="cpu_threshold must be a finite non-negative number"):
        ResourceWatcher(cpu_threshold=math.inf)

def test_watchdog_resource_validation_negative_memory():
    with pytest.raises(ValueError, match="memory_threshold must be a finite non-negative number"):
        ResourceWatcher(memory_threshold=-1.0)

def test_watchdog_resource_validation_nan_memory():
    with pytest.raises(ValueError, match="memory_threshold must be a finite non-negative number"):
        ResourceWatcher(memory_threshold=math.nan)

def test_watchdog_resource_validation_inf_memory():
    with pytest.raises(ValueError, match="memory_threshold must be a finite non-negative number"):
        ResourceWatcher(memory_threshold=math.inf)
