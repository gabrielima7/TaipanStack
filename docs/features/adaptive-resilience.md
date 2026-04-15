# Adaptive Resilience

Resilience is a core principle in TaipanStack. However, statically configured `circuit_breakers` or `retries` can become rigid under varying workloads. TaipanStack v0.4.0 introduces the **Adaptive Resilience** layer.

This module self-tunes in real-time by analyzing success rates and execution outcomes over rolling windows.

---

## Adaptive Circuit Breakers

A standard circuit breaker has a static `failure_threshold`. An **AdaptiveCircuitBreaker** changes its tolerance automatically.

- **High Error Rate**: It lowers its own threshold to trip the circuit faster.
- **Low Error Rate**: It increases its threshold, becoming more tolerant to intermittent drops.

```python
from taipanstack.resilience.adaptive import AdaptiveCircuitBreaker
from taipanstack.core.result import Ok

breaker = AdaptiveCircuitBreaker(
    name="payments-api",
    window_size=100,
    min_throughput=10,
    target_error_rate=0.1,
    recovery_timeout=30.0
)

# You can use it as a standard breaker, but it calculates optimum protection.
if breaker.should_allow():
    try:
        call_api()
        breaker.record_success()
    except Exception as e:
        breaker.record_failure(e)
```

---

## Bulkhead (Concurrency Limiter)

The **Bulkhead** pattern prevents a single failing component from starving the system of resources. By isolating resources, the rest of the app can survive.

```python
from taipanstack.resilience.adaptive import Bulkhead

# Limits up to 10 concurrent requests.
# Anything beyond queue size (50) is immediately rejected.
bulkhead = Bulkhead("heavy-query", max_concurrent=10, max_queue=50)

# Under heavy load, `execute` returns `Err(BulkheadFullError)` instead of locking the thread.
result = await bulkhead.execute(heavy_db_join_query)
```

---

## The Resilience Orchestrator

The ultimate way to secure a dependency is by composing multiple patterns:
1. Limit concurrency to avoid thread exhaustion (*Bulkhead*).
2. Block execution if degraded (*Circuit Breaker*).
3. Retry transient errors with memory (*Adaptive Retry*).
4. Impose a hard deadline (*Timeout*).
5. Default to safe parameters if all fails (*Fallback*).

```python
from taipanstack.core.result import Result
from taipanstack.resilience.adaptive import ResilienceOrchestrator

orch = (
    ResilienceOrchestrator("ai-service")
    .with_bulkhead(max_concurrent=5)
    .with_circuit_breaker(AdaptiveCircuitBreaker("ai", window_size=50))

    .with_fallback({"status": "cached", "data": []})
)

async def fetch_ai_recommendation() -> Result[dict, Exception]:
    # Seamlessly managed execution
    return await orch.execute(ai_client.generate)
```
