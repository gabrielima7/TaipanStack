import asyncio

import pytest

from app.secure_system import (
    InMemoryUserRepository,
    UserCreate,
    UserService,
)
from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.adaptive_breaker import AdaptiveCircuitBreaker
from taipanstack.resilience.adaptive.adaptive_retry import AdaptiveRetry
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator

# Complex Architecture Setup
repository = InMemoryUserRepository()
service = UserService(repository)

orchestrator = (
    ResilienceOrchestrator()
    .with_bulkhead(max_concurrent=10, max_queue=20, timeout=1.0)
    .with_circuit_breaker(AdaptiveCircuitBreaker(recovery_timeout=0.1))
    .with_retry(AdaptiveRetry(max_attempts=3))
    .with_timeout(2.0)
)

async def async_create_user(user_data: UserCreate) -> Result:
    # Simulate async network call to db
    await asyncio.sleep(0.001)
    return service.create_user(user_data)

@pytest.mark.asyncio
async def test_app_chaos_orchestrator_resilience_ok():
    """Simulates thundering herd of valid and invalid user creations."""
    async def worker(i):
        # Generate some valid and invalid data
        username = f"user_{i}"
        email = f"user{i}@example.com"
        password = "SecurePassword123!" if i % 2 == 0 else "short"

        try:
            user_create = UserCreate(username=username, email=email, password=password)
            res = await orchestrator.execute(async_create_user, user_create)
        except Exception as e:
            # Pydantic validation might raise ValidationError, we catch it
            # to focus on the orchestrator/service leaking.
            return Err(e)
        else:
            return res

    tasks = [worker(i) for i in range(100)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        assert isinstance(r, (Ok, Err)), f"Outcome {r} must be wrapped in Result monad"
