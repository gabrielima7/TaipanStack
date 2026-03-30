"""Tests for the context module."""

import asyncio

import pytest

from taipanstack.utils.context import (
    correlation_scope,
    get_correlation_id,
    set_correlation_id,
)


def test_get_set_correlation_id() -> None:
    """Test standard get and set."""
    assert get_correlation_id() is None
    set_correlation_id("test-id-123")
    assert get_correlation_id() == "test-id-123"
    set_correlation_id(None)
    assert get_correlation_id() is None


def test_correlation_scope() -> None:
    """Test correlation scope context manager."""
    set_correlation_id("outer-id")

    with correlation_scope("inner-id"):
        assert get_correlation_id() == "inner-id"

    # Should restore outer context
    assert get_correlation_id() == "outer-id"
    set_correlation_id(None)


@pytest.mark.asyncio
async def test_correlation_id_async_isolation() -> None:
    """Test that correlation IDs are isolated across async tasks."""

    async def worker(worker_id: str, delay: float) -> str | None:
        set_correlation_id(worker_id)
        await asyncio.sleep(delay)
        return get_correlation_id()

    # Create two tasks that will run concurrently
    task1 = asyncio.create_task(worker("worker-1", 0.02))
    task2 = asyncio.create_task(worker("worker-2", 0.01))

    results = await asyncio.gather(task1, task2)

    assert results == ["worker-1", "worker-2"]

    # Assert that the main context is not polluted
    # If the environment was clean before this test, it should be None,
    # but to be safe and avoid flakiness, we just assert it didn't
    # leak from the async contexts.
    assert get_correlation_id() not in ["worker-1", "worker-2"]
