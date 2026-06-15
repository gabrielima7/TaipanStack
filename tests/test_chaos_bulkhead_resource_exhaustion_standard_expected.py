from unittest.mock import AsyncMock, patch

import pytest

from taipanstack.core.result import Err
from taipanstack.resilience.adaptive.bulkhead import Bulkhead


@pytest.mark.asyncio
async def test_chaos_bulkhead_resource_exhaustion_bulkhead_semaphore_exhaustion_chaos_returns_err_standard_expected() -> (
    None
):
    bulkhead = Bulkhead("test_chaos", max_concurrent=2, max_queue=2)

    async def dummy_task() -> int:
        return 42

    with patch.object(
        bulkhead._semaphore, "acquire", new_callable=AsyncMock
    ) as mock_acquire:
        mock_acquire.side_effect = OSError("Too many open files")

        result = await bulkhead.execute(dummy_task)

        assert isinstance(result, Err)
        assert isinstance(result.err_value, BaseException)
        assert "Resource exhaustion" in str(result.err_value)
