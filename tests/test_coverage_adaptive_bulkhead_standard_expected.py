import asyncio
import contextlib

import pytest

from taipanstack.core.result import Err
from taipanstack.resilience.adaptive.bulkhead import Bulkhead


@pytest.mark.asyncio
async def test_bulkhead_wait_for_permit_timeout():
    bulk = Bulkhead("test", max_concurrent=1, timeout=0.01)

    async def blocking():
        await asyncio.sleep(0.1)

    t1 = asyncio.create_task(bulk.execute(blocking))
    await asyncio.sleep(0.005)

    result = await bulk.execute(blocking)
    assert isinstance(result, Err)

    t1.cancel()
    with contextlib.suppress(Exception, asyncio.CancelledError):
        await t1
