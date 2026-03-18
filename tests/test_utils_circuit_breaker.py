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
