import pytest
from taipanstack.bridges.web_bridge import result_to_response
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.resilience.watchdogs.config_watcher import ConfigWatcher
from taipanstack.resilience.watchdogs.health_pinger import HealthPinger, HealthTarget, check_all
from taipanstack.resilience.watchdogs.resource_watcher import ResourceWatcher
from taipanstack.security.types import _validate_safe_url
from taipanstack.utils.cache import cached
from taipanstack.security.guards import guard_ssrf
from taipanstack.core.result import Ok
from pydantic import BaseModel
from pathlib import Path
from unittest.mock import patch
import asyncio

def test_web_bridge_match():
    with pytest.raises(TypeError):
        result_to_response("Not a Result")

def test_adaptive_breaker_match():
    breaker = AdaptiveCircuitBreaker()
    with pytest.raises(TypeError):
        breaker.evaluate_result("Not a result")

@pytest.mark.asyncio
async def test_orchestrator_match():
    orch = ResilienceOrchestrator("test").with_fallback("default")
    with pytest.raises(TypeError):
        orch._apply_fallback("Not a result")

    with patch("taipanstack.resilience.adaptive.orchestrator.ResilienceOrchestrator._execute_with_timeout", return_value="Not a result"):
        # `match result` on `result` should raise TypeError.
        # But `_execute_inner` catches nothing in its logic around the match so it bubbles up.
        with pytest.raises(TypeError):
            await orch._execute_inner(lambda: 1)

class DummyModel(BaseModel):
    pass

def test_config_watcher_match():
    watcher = ConfigWatcher(config_paths=[Path("test")], config_model=DummyModel)
    with patch("taipanstack.resilience.watchdogs.config_watcher._load_file_data", return_value="Not a result"):
        with pytest.raises(TypeError):
            watcher._validate_and_apply(Path("test"))
    with patch("taipanstack.resilience.watchdogs.config_watcher._hash_file", return_value="Not a result"):
        with pytest.raises(TypeError):
            watcher._detect_changes()

    with patch("taipanstack.resilience.watchdogs.config_watcher._load_file_data", return_value=Ok({"dummy": "data"})), patch("taipanstack.resilience.watchdogs.config_watcher.validate_config", return_value="Not a result"):
        with pytest.raises(TypeError):
            watcher._validate_and_apply(Path("test"))

@pytest.mark.asyncio
async def test_health_pinger_match():
    async def dummy_check(): return True
    target = HealthTarget(name="test", check=dummy_check)
    with patch("taipanstack.resilience.watchdogs.health_pinger.check_target", return_value="Not a result"):
        with pytest.raises(TypeError):
            await check_all([target])

    pinger = HealthPinger(targets=[target])
    with patch("taipanstack.resilience.watchdogs.health_pinger.check_target", return_value="Not a result"):
        with pytest.raises(TypeError):
            await pinger._run()

@pytest.mark.asyncio
async def test_resource_watcher_match():
    watcher = ResourceWatcher()
    with patch("taipanstack.resilience.watchdogs.resource_watcher.check_resources", return_value="Not a result"):
        with pytest.raises(TypeError):
            await watcher._run()

def test_security_types_match():
    with patch("taipanstack.security.types.guard_ssrf", return_value="Not a result"):
        with pytest.raises(TypeError):
            _validate_safe_url("http://test")

def test_security_guards_match():
    with patch("taipanstack.security.guards._validate_ssrf_url", return_value="Not a result"):
        with pytest.raises(TypeError):
            guard_ssrf("http://test")
    with patch("taipanstack.security.guards._check_ip_safety", return_value="Not a result"):
        # The first match returns Ok(hostname), and then we mock _check_ip_safety.
        # To trigger the second match failure, _validate_ssrf_url must return an Ok.
        with patch("taipanstack.security.guards._validate_ssrf_url", return_value=Ok("hostname")):
            with pytest.raises(TypeError):
                guard_ssrf("http://test")

@pytest.mark.asyncio
async def test_cache_match():
    @cached(ttl=1)
    async def my_async():
        return "Not a result"

    @cached(ttl=1)
    def my_sync():
        return "Not a result"

    with pytest.raises(TypeError):
        await my_async()
    with pytest.raises(TypeError):
        my_sync()
