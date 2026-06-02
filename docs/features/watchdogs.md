# Active Monitoring (Watchdogs)

In a microservices environment, assuming services are healthy until they fail is dangerous. To implement proactive security, **Watchdogs** act as specialized background watchers that preemptively lock down integrations when anomalies are detected.

---

## Health Pinger

The `HealthPinger` polls your external dependencies (APIs, DBs, caches). If they drop, it artificially trips their associated `CircuitBreaker`.

This guarantees that application endpoints calling the DB won't even try and timeout; they will instantly return a circuit breaker failure, saving massive CPU cycles.

```python
import asyncio
from taipanstack.resilience.watchdogs import HealthPinger, HealthTarget
from taipanstack.resilience.circuit_breaker import CircuitBreaker

db_breaker = CircuitBreaker("pg-db")

async def check_db() -> bool:
    try:
        # Fast query
        return True
    except Exception:
        return False

# Runs every 5 seconds
pinger = HealthPinger(
    interval=5.0,
    targets=[
        HealthTarget(name="database", check=check_db, circuit_breaker=db_breaker)
    ],
    on_health_change=lambda name, healthy: print(f"{name} is now {healthy}")
)

# Run in background via asyncio.create_task()
background_task = asyncio.create_task(pinger.start())
```

---

## Resource Watcher

The `ResourceWatcher` taps into `psutil` keeping track of the hardware limits of your host or container. It offers real-time signals when CPU or Memory surpasses threshold targets.

```python
from taipanstack.resilience.watchdogs import ResourceWatcher

def on_threshold_breach(resource: str, value: float):
    print(f"CRITICAL ALARM: {resource} is at {value}%")

# Create a watcher configured to alarm at 90% CPU usage or 95% RAM
watcher = ResourceWatcher(
    interval=2.0,
    cpu_threshold=90.0,
    memory_threshold=95.0,
    on_threshold_breach=on_threshold_breach
)

background_task = asyncio.create_task(watcher.start())
```

---

## Config Watcher

Environment drift and configuration file tampering are common deployment blindspots. Use the `ConfigWatcher` to watch a `.env` or `.toml` file and trigger application reloads or alerts.


```python
from pydantic import BaseModel
from taipanstack.resilience.watchdogs import ConfigWatcher

class MyConfig(BaseModel):
    debug: bool
    max_connections: int

def hot_reload(file_path: str, new_hash: str):
    print(f"Config {file_path} changed! Reloading...")

# Watches config.json using cryptographic SHA-256 fingerprinting and validates with MyConfig
config_watcher = ConfigWatcher(
    config_paths=["config.json"],
    config_model=MyConfig,
    interval=10.0,
    on_config_change=hot_reload
)

background_task = asyncio.create_task(config_watcher.start())
```
