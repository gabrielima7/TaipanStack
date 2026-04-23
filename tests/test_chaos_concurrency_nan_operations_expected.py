import pytest

from taipanstack.utils.concurrency import limit_concurrency


def test_chaos_concurrency_rejects_nan_timeout_expected():
    """Chaos test: Inject NaN for timeout in sync concurrency limiter."""
    with pytest.raises(ValueError, match="timeout must be >= 0.0 and finite"):
        @limit_concurrency(max_tasks=1, timeout=float("nan"))
        def my_func():
            return "ok"

def test_chaos_concurrency_rejects_inf_timeout_expected():
    """Chaos test: Inject Inf for timeout in sync concurrency limiter."""
    with pytest.raises(ValueError, match="timeout must be >= 0.0 and finite"):
        @limit_concurrency(max_tasks=1, timeout=float("inf"))
        def my_func():
            return "ok"

def test_chaos_concurrency_rejects_nan_max_tasks_expected():
    """Chaos test: Inject NaN for max_tasks in sync concurrency limiter."""
    with pytest.raises(TypeError):
        @limit_concurrency(max_tasks=float("nan"), timeout=1.0)
        def my_func():
            return "ok"

def test_chaos_concurrency_rejects_inf_max_tasks_expected():
    """Chaos test: Inject Inf for max_tasks in sync concurrency limiter."""
    with pytest.raises(TypeError):
        @limit_concurrency(max_tasks=float("inf"), timeout=1.0)
        def my_func():
            return "ok"
def test_chaos_concurrency_rejects_bool_max_tasks_expected():
    """Chaos test: Inject boolean for max_tasks in sync concurrency limiter."""
    with pytest.raises(TypeError, match="must be an integer"):
        @limit_concurrency(max_tasks=True, timeout=1.0) # type: ignore
        def my_func():
            return "ok"
