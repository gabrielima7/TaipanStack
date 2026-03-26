"""Watchdog sub-package for TaipanStack resilience.

Provides background monitors that proactively detect and respond
to system degradation: resource pressure, configuration drift,
and dependency failures.
"""

from taipanstack.resilience.watchdogs._base import BaseWatcher
from taipanstack.resilience.watchdogs.config_watcher import (
    ConfigWatcher,
    validate_config,
)
from taipanstack.resilience.watchdogs.health_pinger import (
    HealthPinger,
    HealthTarget,
    check_all,
    check_target,
)
from taipanstack.resilience.watchdogs.resource_watcher import (
    ResourceSnapshot,
    ResourceWatcher,
    check_resources,
)

__all__ = (
    "BaseWatcher",
    "ConfigWatcher",
    "HealthPinger",
    "HealthTarget",
    "ResourceSnapshot",
    "ResourceWatcher",
    "check_all",
    "check_resources",
    "check_target",
    "validate_config",
)
