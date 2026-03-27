with open("src/taipanstack/resilience/adaptive/orchestrator.py", "r") as f:
    content = f.read()

content = content.replace("from typing import Any, Callable, Coroutine, TypeVar, cast", "from typing import Any, Callable, Coroutine, Generic, TypeVar, cast")
content = content.replace("class ResilienceOrchestrator:", "class ResilienceOrchestrator(Generic[T]):")

content = content.replace("def with_bulkhead(\n        self,\n        max_concurrent: int = 10,\n        max_queue: int = 50,\n        timeout: float = 30.0,\n    ) -> ResilienceOrchestrator:", "def with_bulkhead(\n        self,\n        max_concurrent: int = 10,\n        max_queue: int = 50,\n        timeout: float = 30.0,\n    ) -> ResilienceOrchestrator[T]:")
content = content.replace("def with_circuit_breaker(\n        self,\n        breaker: CircuitBreaker | AdaptiveCircuitBreaker,\n    ) -> ResilienceOrchestrator:", "def with_circuit_breaker(\n        self,\n        breaker: CircuitBreaker | AdaptiveCircuitBreaker,\n    ) -> ResilienceOrchestrator[T]:")
content = content.replace("def with_retry(\n        self,\n        config: RetryConfig | AdaptiveRetry,\n    ) -> ResilienceOrchestrator:", "def with_retry(\n        self,\n        config: RetryConfig | AdaptiveRetry,\n    ) -> ResilienceOrchestrator[T]:")
content = content.replace("def with_timeout(self, seconds: float) -> ResilienceOrchestrator:", "def with_timeout(self, seconds: float) -> ResilienceOrchestrator[T]:")
content = content.replace("def with_fallback(self, value: T) -> ResilienceOrchestrator:", "def with_fallback(self, value: T) -> ResilienceOrchestrator[T]:")

with open("src/taipanstack/resilience/adaptive/orchestrator.py", "w") as f:
    f.write(content)
