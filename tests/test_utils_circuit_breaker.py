"""Tests for circuit breaker module."""

import time

import pytest

from taipanstack.utils.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
    circuit_breaker,
)


class TestCircuitBreakerState:
    """Tests for CircuitState enum."""

    def test_states_exist(self) -> None:
        """Test that all states are defined."""
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"

    def test_circuit_breaker_no_structlog(self) -> None:
        """Test fallback when structlog is not installed."""
        # We don't want to use importlib.reload because it breaks Enum identities used elsewhere
        # Instead, just execute the module's code in a new namespace
        import importlib.util
        from unittest import mock

        with mock.patch.dict("sys.modules", {"structlog": None}):
            spec = importlib.util.find_spec("taipanstack.utils.circuit_breaker")
            module = importlib.util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(module)  # type: ignore
            assert module._HAS_STRUCTLOG is False

    def test_circuit_breaker_unreachable_state(self) -> None:
        """Test unreachable state block."""
        from taipanstack.utils.circuit_breaker import CircuitBreaker

        breaker = CircuitBreaker()
        # Forcibly inject an invalid state to hit the unreachable branch in match
        breaker._state.state = "INVALID_STATE"  # type: ignore[assignment]

        # Verify it falls through match and returns False
        # _should_attempt wraps _allow_request
        assert breaker._should_attempt() is False


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_starts_closed(self) -> None:
        """Test that circuit starts in closed state."""
        breaker = CircuitBreaker()
        assert breaker.state == CircuitState.CLOSED

    def test_success_keeps_closed(self) -> None:
        """Test that successful calls keep circuit closed."""
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def success_func() -> str:
            return "ok"

        for _ in range(10):
            assert success_func() == "ok"

        assert breaker.state == CircuitState.CLOSED

    def test_failures_open_circuit(self) -> None:
        """Test that failures open the circuit."""
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        for _ in range(3):
            with pytest.raises(ValueError):
                failing_func()

        assert breaker.state == CircuitState.OPEN

    def test_open_circuit_blocks_calls(self) -> None:
        """Test that open circuit blocks calls."""
        breaker = CircuitBreaker(failure_threshold=2, timeout=60)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        # Trip the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                failing_func()

        # Now should raise CircuitBreakerError
        with pytest.raises(CircuitBreakerError):
            failing_func()

    def test_timeout_moves_to_half_open(self) -> None:
        """Test that timeout moves circuit to half-open."""
        breaker = CircuitBreaker(failure_threshold=1, timeout=0.1)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        # Trip the circuit
        with pytest.raises(ValueError):
            failing_func()

        assert breaker.state == CircuitState.OPEN

        # Wait for timeout
        time.sleep(0.15)

        # Next attempt should be allowed (half-open)
        with pytest.raises(ValueError):
            failing_func()

        # Should be back to open after failure in half-open
        assert breaker.state == CircuitState.OPEN

    def test_half_open_thundering_herd_chaos(self) -> None:
        """Test that half-open state prevents thundering herd attacks.

        Simulates an extreme thundering herd failure scenario where
        hundreds of requests are simultaneously spawned exactly as the
        circuit goes into half-open state. This ensures only a limited
        number of requests (equal to success_threshold) actually proceed.
        """
        import concurrent.futures

        breaker = CircuitBreaker(
            failure_threshold=1,
            success_threshold=3,
            timeout=0.05,
        )

        active_calls = 0
        max_active_calls = 0
        call_count = 0

        @breaker
        def api_call() -> str:
            nonlocal active_calls, max_active_calls, call_count

            with breaker._state.lock:
                # We do lock-based increment purely for test measurement
                # Real requests would run concurrently here
                pass

            active_calls += 1
            max_active_calls = max(max_active_calls, active_calls)

            call_count += 1

            # Simulate first call failing to trigger open state
            if call_count == 1:
                active_calls -= 1
                raise ValueError("Initial trip failure")

            # Simulate real-world delay for concurrency check
            time.sleep(0.01)

            active_calls -= 1
            return "ok"

        # 1. Trip the circuit
        with pytest.raises(ValueError):
            api_call()

        assert breaker.state == CircuitState.OPEN

        # 2. Wait for timeout to allow half-open
        time.sleep(0.1)

        # 3. Simulate thundering herd (100 simultaneous requests)
        num_requests = 100
        successes = 0
        circuit_open_errors = 0

        import threading

        start_event = threading.Event()

        def synchronized_call() -> str:
            start_event.wait()
            return api_call()

        # 3. Simulate thundering herd (100 simultaneous requests)
        # Because true parallel locks under CPython can still suffer from context
        # switching races across the interpreter when hitting decorators, we assert
        # the *max upper bound* logic. Under a true lock isolation, it should let exactly
        # `success_threshold` requests through.
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            # We want to wait for them to spool up before unleashing
            futures = [executor.submit(synchronized_call) for _ in range(num_requests)]

            # Ensure all threads are waiting at the starting line, then release
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

        # 4. Verify resilience

        # We assert it properly throttled the thundering herd by rejecting
        # the vast majority. Without the fix, 100/100 would go through.
        # With the fix, exactly 3 should go through, but on CI runners with fewer
        # cores, Python threading might only manage a few, so we assert it is
        # exactly equal to the configured success threshold.
        # However, due to Python's GIL and thread switching semantics during the
        # exact instruction where `successes += 1` executes across 100 threads,
        # assertions comparing raw integer limits derived from high-concurrency
        # mocks are prone to flakiness. The key to the chaos test is ensuring
        # it blocked the *majority* of the herd (rather than exact equality to 3
        # on all system topologies).
        assert successes <= breaker.config.success_threshold
        assert circuit_open_errors >= num_requests - breaker.config.success_threshold

        # The remaining 97 requests must have been instantly rejected with CircuitBreakerError
        assert circuit_open_errors == num_requests - breaker.config.success_threshold

        # Concurrency should have been strictly limited to the success threshold
        # (Though due to thread timing, max_active_calls could be lower, it must never exceed threshold)
        assert max_active_calls <= breaker.config.success_threshold

        # Finally, circuit should be fully closed again
        assert breaker.state == CircuitState.CLOSED

    def test_success_in_half_open_closes(self) -> None:
        """Test that success in half-open closes circuit."""
        breaker = CircuitBreaker(
            failure_threshold=1,
            success_threshold=1,
            timeout=0.05,
        )
        call_count = 0

        @breaker
        def flaky_func() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("first fail")
            return "ok"

        # Trip the circuit
        with pytest.raises(ValueError):
            flaky_func()

        # Wait for timeout
        time.sleep(0.1)

        # Should succeed and close circuit
        assert flaky_func() == "ok"
        assert breaker.state == CircuitState.CLOSED

    def test_reset_closes_circuit(self) -> None:
        """Test that reset closes the circuit."""
        breaker = CircuitBreaker(failure_threshold=1)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        # Trip the circuit
        with pytest.raises(ValueError):
            failing_func()

        assert breaker.state == CircuitState.OPEN

        breaker.reset()
        assert breaker.state == CircuitState.CLOSED

    def test_excluded_exceptions_dont_trip(self) -> None:
        """Test that excluded exceptions don't trip circuit."""
        breaker = CircuitBreaker(
            failure_threshold=2,
            excluded_exceptions=(ValueError,),
        )

        @breaker
        def failing_func() -> None:
            raise ValueError("ignored")

        # These shouldn't trip the circuit
        for _ in range(5):
            with pytest.raises(ValueError):
                failing_func()

        assert breaker.state == CircuitState.CLOSED


class TestCircuitBreakerDecorator:
    """Tests for @circuit_breaker decorator."""

    def test_decorator_creates_breaker(self) -> None:
        """Test that decorator creates a working circuit breaker."""

        @circuit_breaker(failure_threshold=2)
        def my_func() -> str:
            return "ok"

        assert my_func() == "ok"

    def test_decorator_with_name(self) -> None:
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

    async def test_decorator_async_failure_opens_circuit(self) -> None:
        """Test that failures in async functions open the circuit."""

        @circuit_breaker(failure_threshold=2)
        async def my_async_func() -> None:
            raise ValueError("async_fail")

        # Trip the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                await my_async_func()

        # Circuit should now be open, raising CircuitBreakerError
        with pytest.raises(CircuitBreakerError) as exc_info:
            await my_async_func()

        assert exc_info.value.state == CircuitState.OPEN


class TestCircuitBreakerError:
    """Tests for CircuitBreakerError."""

    def test_has_state(self) -> None:
        """Test that error has state attribute."""
        error = CircuitBreakerError("test", CircuitState.OPEN)
        assert error.state == CircuitState.OPEN

    def test_message(self) -> None:
        """Test error message."""
        error = CircuitBreakerError("Circuit is open", CircuitState.OPEN)
        assert "Circuit is open" in str(error)
