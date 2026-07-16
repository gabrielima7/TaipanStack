import math

import pytest

from taipanstack.resilience.watchdogs.health_pinger import HealthPinger


def test_watchdog_health_validation_negative_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        HealthPinger(targets=[], interval=-1.0)

def test_watchdog_health_validation_zero_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        HealthPinger(targets=[], interval=0.0)

def test_watchdog_health_validation_nan_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        HealthPinger(targets=[], interval=math.nan)

def test_watchdog_health_validation_inf_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        HealthPinger(targets=[], interval=math.inf)
