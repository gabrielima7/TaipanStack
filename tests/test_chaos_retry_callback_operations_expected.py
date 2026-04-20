import sys

import pytest

from taipanstack.resilience.retry import retry


def test_chaos_retry_callback_retry_chaos_faulty_callback_expected():
    def faulty_callback(attempt, max_attempts, exc, delay):
        raise ValueError("Simulated callback failure")

    @retry(max_attempts=3, on_retry=faulty_callback)
    def failing_service():
        raise RuntimeError("Service failure")

    with pytest.raises(Exception, match="All 3 attempts failed for failing_service"):
        failing_service()

    state = {"calls": 0}

    @retry(max_attempts=3, on_retry=faulty_callback)
    def recovering_service():
        state["calls"] += 1
        if state["calls"] < 2:
            raise RuntimeError("Temporary failure")
        return "success"

    assert recovering_service() == "success"


def test_chaos_retry_callback_retry_chaos_faulty_callback_without_structlog_expected(monkeypatch):
    monkeypatch.setattr(
        sys.modules["taipanstack.resilience.retry"], "_HAS_STRUCTLOG", False
    )

    def faulty_callback(attempt, max_attempts, exc, delay):
        raise ValueError("Simulated failure without structlog")

    @retry(max_attempts=3, on_retry=faulty_callback)
    def failing_service():
        raise RuntimeError("Service failure")

    with pytest.raises(Exception, match="All 3 attempts failed for failing_service"):
        failing_service()
