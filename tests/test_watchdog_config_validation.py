import math

import pytest
from pydantic import BaseModel

from taipanstack.resilience.watchdogs.config_watcher import ConfigWatcher


class DummyModel(BaseModel):
    pass


def test_watchdog_config_validation_negative_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ConfigWatcher(config_paths=[], config_model=DummyModel, interval=-1.0)


def test_watchdog_config_validation_zero_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ConfigWatcher(config_paths=[], config_model=DummyModel, interval=0.0)


def test_watchdog_config_validation_nan_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ConfigWatcher(config_paths=[], config_model=DummyModel, interval=math.nan)


def test_watchdog_config_validation_inf_interval():
    with pytest.raises(ValueError, match="interval must be a finite positive number"):
        ConfigWatcher(config_paths=[], config_model=DummyModel, interval=math.inf)
