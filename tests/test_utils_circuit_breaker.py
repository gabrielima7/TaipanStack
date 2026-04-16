"""Tests for circuit breaker module."""

import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
    circuit_breaker,
)


class TestCircuitBreakerState:
    """Tests for CircuitState enum."""

    def test_utils_circuit_breaker_states_exist_expected(self) -> None:
        """Test that all states are defined."""
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"

    def test_circuit_breaker_no_structlog_expected(self) -> None:
        """Test fallback when structlog is not installed."""
        import importlib.util
        from unittest import mock

        with mock.patch.dict("sys.modules", {"structlog": None}):
            spec = importlib.util.find_spec("taipanstack.resilience.circuit_breaker")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            assert module._HAS_STRUCTLOG is False

    def test_circuit_breaker_unreachable_state_expected(self) -> None:
        """Test unreachable state block."""
        from taipanstack.resilience.circuit_breaker import CircuitBreaker

        breaker = CircuitBreaker()
        breaker._state.state = "INVALID_STATE"
        assert breaker._should_attempt() is False


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_utils_circuit_breaker_starts_closed_expected(self) -> None:
        """Test that circuit starts in closed state."""
        breaker = CircuitBreaker()
        assert breaker.state == CircuitState.CLOSED

    def test_success_keeps_closed_expected(self) -> None:
        """Test that successful calls keep circuit closed."""
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def success_func() -> str:
            return "ok"

        for _ in range(10):
            assert success_func() == "ok"
        assert breaker.state == CircuitState.CLOSED

    def test_failures_open_circuit_expected(self) -> None:
        """Test that failures open the circuit."""
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        for _ in range(3):
            with pytest.raises(ValueError):
                failing_func()
        assert breaker.state == CircuitState.OPEN

    def test_open_circuit_blocks_calls_expected(self) -> None:
        """Test that open circuit blocks calls."""
        breaker = CircuitBreaker(failure_threshold=2, timeout=60)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        for _ in range(2):
            with pytest.raises(ValueError):
                failing_func()
        with pytest.raises(CircuitBreakerError):
            failing_func()

    def test_timeout_moves_to_half_open_expected(self) -> None:
        """Test that timeout moves circuit to half-open."""
        breaker = CircuitBreaker(failure_threshold=1, timeout=0.1)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        with pytest.raises(ValueError):
            failing_func()
        assert breaker.state == CircuitState.OPEN
        time.sleep(0.15)
        with pytest.raises(ValueError):
            failing_func()
        assert breaker.state == CircuitState.OPEN

    def test_half_open_thundering_herd_chaos_expected(self) -> None:
        """Test that half-open state prevents thundering herd attacks.

        Simulates an extreme thundering herd failure scenario where
        hundreds of requests are simultaneously spawned exactly as the
        circuit goes into half-open state. This ensures only a limited
        number of requests (equal to success_threshold) actually proceed.
        """
        import concurrent.futures

        breaker = CircuitBreaker(failure_threshold=1, success_threshold=3, timeout=0.05)
        active_calls = 0
        max_active_calls = 0
        call_count = 0

        @breaker
        def api_call() -> str:
            nonlocal active_calls, max_active_calls, call_count
            with breaker._state.lock:
                pass
            active_calls += 1
            max_active_calls = max(max_active_calls, active_calls)
            call_count += 1
            if call_count == 1:
                active_calls -= 1
                raise ValueError("Initial trip failure")
            time.sleep(0.5)
            active_calls -= 1
            return "ok"

        with pytest.raises(ValueError):
            api_call()
        assert breaker.state == CircuitState.OPEN
        time.sleep(0.1)
        num_requests = 100
        successes = 0
        circuit_open_errors = 0
        import threading

        start_event = threading.Event()

        def synchronized_call() -> str:
            start_event.wait()
            return api_call()

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(synchronized_call) for _ in range(num_requests)]
            time.sleep(0.1)
            start_event.set()
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result == "ok":
                        successes += 1
                except CircuitBreakerError:
                    circuit_open_errors += 1
                except Exception as e:
                    pytest.fail(f"Unexpected exception: {e}")
        assert successes <= breaker.config.success_threshold
        assert circuit_open_errors >= num_requests - breaker.config.success_threshold
        assert circuit_open_errors == num_requests - breaker.config.success_threshold
        assert max_active_calls <= breaker.config.success_threshold
        assert breaker.state == CircuitState.CLOSED

    def test_success_in_half_open_closes_expected(self) -> None:
        """Test that success in half-open closes circuit."""
        breaker = CircuitBreaker(failure_threshold=1, success_threshold=1, timeout=0.05)
        call_count = 0

        @breaker
        def flaky_func() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("first fail")
            return "ok"

        with pytest.raises(ValueError):
            flaky_func()
        time.sleep(0.1)
        assert flaky_func() == "ok"
        assert breaker.state == CircuitState.CLOSED

    def test_reset_closes_circuit_expected(self) -> None:
        """Test that reset closes the circuit."""
        breaker = CircuitBreaker(failure_threshold=1)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        with pytest.raises(ValueError):
            failing_func()
        assert breaker.state == CircuitState.OPEN
        breaker.reset()
        assert breaker.state == CircuitState.CLOSED

    def test_excluded_exceptions_dont_trip_expected(self) -> None:
        """Test that excluded exceptions don't trip circuit."""
        breaker = CircuitBreaker(failure_threshold=2, excluded_exceptions=(ValueError,))

        @breaker
        def failing_func() -> None:
            raise ValueError("ignored")

        for _ in range(5):
            with pytest.raises(ValueError):
                failing_func()
        assert breaker.state == CircuitState.CLOSED


class TestCircuitBreakerDecorator:
    """Tests for @circuit_breaker decorator."""

    def test_decorator_creates_breaker_expected(self) -> None:
        """Test that decorator creates a working circuit breaker."""

        @circuit_breaker(failure_threshold=2)
        def my_func() -> str:
            return "ok"

        assert my_func() == "ok"

    def test_decorator_with_name_expected(self) -> None:
        """Test that decorator accepts custom name."""

        @circuit_breaker(failure_threshold=2, name="custom_breaker")
        def my_func() -> str:
            return "ok"

        assert my_func() == "ok"

    async def test_decorator_async_success(self) -> None:
        """Test that decorator works with async functions."""

        @circuit_breaker(failure_threshold=2)
        async def my_async_func() -> str:
            return "async_ok"

        assert await my_async_func() == "async_ok"

    async def test_decorator_async_failure_opens_circuit_expected(self) -> None:
        """Test that failures in async functions open the circuit."""

        @circuit_breaker(failure_threshold=2)
        async def my_async_func() -> None:
            raise ValueError("async_fail")

        for _ in range(2):
            with pytest.raises(ValueError):
                await my_async_func()
        with pytest.raises(CircuitBreakerError) as exc_info:
            await my_async_func()
        assert exc_info.value.state == CircuitState.OPEN


class TestCircuitBreakerError:
    """Tests for CircuitBreakerError."""

    def test_utils_circuit_breaker_has_state_expected(self) -> None:
        """Test that error has state attribute."""
        error = CircuitBreakerError("test", CircuitState.OPEN)
        assert error.state == CircuitState.OPEN

    def test_utils_circuit_breaker_message_expected(self) -> None:
        """Test error message."""
        error = CircuitBreakerError("Circuit is open", CircuitState.OPEN)
        assert "Circuit is open" in str(error)
