import pytest

from taipanstack.resilience.adaptive.bulkhead import Bulkhead


@pytest.mark.asyncio
async def test_chaos_bulkhead_lock_acquire_exception_expected():
    bulkhead = Bulkhead(max_concurrent=1, max_queue=1)

    class BadSemaphore:
        async def acquire(self):
            raise RuntimeError("Chaos lock acquire error")

        def release(self):
            return None

    bulkhead._semaphore = BadSemaphore()

    async def dummy():
        return True

    result = await bulkhead.execute(dummy)
    assert result.is_err()
    assert "Resource exhaustion" in str(result.unwrap_err())
