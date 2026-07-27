import threading
from unittest.mock import patch

import pytest

from taipanstack.utils.concurrency import OverloadError, limit_concurrency


@pytest.mark.asyncio
async def test_chaos_concurrency_timeout_mutation_concurrency_async_timeout_mutation():
    @limit_concurrency(max_tasks=1, timeout=1.0)
    async def fast_op():
        return "success"

    with patch("asyncio.timeout", side_effect=TypeError("Mocked TypeError in timeout")):
        res = await fast_op()
        assert res.is_err()
        assert isinstance(res.unwrap_err(), OverloadError)
        assert "Resource exhaustion" in str(res.unwrap_err())


def test_chaos_concurrency_timeout_mutation_concurrency_sync_timeout_mutation_expected():
    @limit_concurrency(max_tasks=1, timeout=1.0)
    def fast_op_sync():
        return "success"

    with patch.object(
        threading.Semaphore, "acquire", side_effect=TypeError("Mocked TypeError")
    ):
        res = fast_op_sync()
        assert res.is_err()
        assert isinstance(res.unwrap_err(), OverloadError)
        assert "Resource exhaustion" in str(res.unwrap_err())


def test_chaos_concurrency_timeout_mutation_concurrency_timeout_type_mutation_expected():
    with pytest.raises(
        ValueError, match="timeout must be a finite non-negative number"
    ):

        @limit_concurrency(max_tasks=1, timeout="string")  # type: ignore
        def fast_op():
            return "success"


def test_chaos_concurrency_timeout_mutation_concurrency_max_tasks_type_mutation_expected():
    with pytest.raises(ValueError, match="max_tasks must be > 0"):

        @limit_concurrency(max_tasks="string", timeout=1.0)  # type: ignore
        def fast_op2():
            return "success"
