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

    def test_utils_circuit_breaker_states_exist(self) -> None:
        """Test that all states are defined."""
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"

    def test_utils_circuit_breaker_circuit_breaker_no_structlog(self) -> None:
        """Test fallback when structlog is not installed."""
        # We don't want to use importlib.reload because it breaks Enum identities used elsewhere
        # Instead, just execute the module's code in a new namespace
        import importlib.util
        from unittest import mock

        with mock.patch.dict("sys.modules", {"structlog": None}):
            spec = importlib.util.find_spec("taipanstack.resilience.circuit_breaker")
            module = importlib.util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(module)  # type: ignore
            assert module._HAS_STRUCTLOG is False

    def test_utils_circuit_breaker_circuit_breaker_unreachable_state(
        self,
    ) -> None:
        """Test unreachable state block."""
        from taipanstack.resilience.circuit_breaker import CircuitBreaker

        breaker = CircuitBreaker()
        # Forcibly inject an invalid state to hit the unreachable branch in match
        breaker._state.state = "INVALID_STATE"  # type: ignore[assignment]

        # Verify it falls through match and returns False
        # _should_attempt wraps _allow_request
        assert breaker._should_attempt() is False


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_utils_circuit_breaker_starts_closed(self) -> None:
        """Test that circuit starts in closed state."""
        breaker = CircuitBreaker()
        assert breaker.state == CircuitState.CLOSED

    def test_utils_circuit_breaker_success_keeps_closed(self) -> None:
        """Test that successful calls keep circuit closed."""
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def success_func() -> str:
            return "ok"

        for _ in range(10):
            assert success_func() == "ok"

        assert breaker.state == CircuitState.CLOSED

    def test_utils_circuit_breaker_failures_open_circuit(self) -> None:
        """Test that failures open the circuit."""
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def failing_func() -> None:
            raise ValueError("fail")

        for _ in range(3):
            with pytest.raises(ValueError):
                failing_func()

        assert breaker.state == CircuitState.OPEN

    def test_utils_circuit_breaker_open_circuit_blocks_calls(self) -> None:
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

    def test_utils_circuit_breaker_timeout_moves_to_half_open(self) -> None:
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

    def test_utils_circuit_breaker_half_open_thundering_herd_chaos(
        self,
    ) -> None:
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
                assert True

            active_calls += 1
            max_active_calls = max(max_active_calls, active_calls)

            call_count += 1

            # Simulate first call failing to trigger open state
            if call_count == 1:
                active_calls -= 1
                raise ValueError("Initial trip failure")

            # Simulate real-world delay for concurrency check
            # We use a longer sleep (0.5) to ensure all threads get a chance to
            # hit the state evaluation logic before any one thread completes and
            # mutates the circuit state.
            time.sleep(0.5)

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

    def test_utils_circuit_breaker_success_in_half_open_closes(self) -> None:
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

    def test_utils_circuit_breaker_reset_closes_circuit(self) -> None:
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

    def test_utils_circuit_breaker_excluded_exceptions_dont_trip(self) -> None:
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

    def test_utils_circuit_breaker_decorator_creates_breaker(self) -> None:
        """Test that decorator creates a working circuit breaker."""

        @circuit_breaker(failure_threshold=2)
        def my_func() -> str:
            return "ok"

        assert my_func() == "ok"

    def test_utils_circuit_breaker_decorator_with_name(self) -> None:
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

    def test_utils_circuit_breaker_has_state(self) -> None:
        """Test that error has state attribute."""
        error = CircuitBreakerError("test", CircuitState.OPEN)
        assert error.state == CircuitState.OPEN

    def test_utils_circuit_breaker_message(self) -> None:
        """Test error message."""
        error = CircuitBreakerError("Circuit is open", CircuitState.OPEN)
        assert "Circuit is open" in str(error)


# Migrated from tests/test_chaos_circuit_breaker_clock_jump_operations.py


def test_chaos_circuit_breaker_clock_jump_circuit_breaker_backward_clock_jump_chaos(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Simulate a backward clock jump (NTP anomaly) keeping circuit OPEN forever."""
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    time_val = 1000.0
    monkeypatch.setattr(time, "monotonic", lambda: time_val)

    @breaker
    def failing_func():
        raise ValueError("Fail")

    with pytest.raises(ValueError):
        failing_func()

    assert breaker.state == CircuitState.OPEN

    # Clock jumps backward by 1 day!
    time_val = 1000.0 - 86400.0

    # Wait for the normal timeout (10 seconds)
    time_val += 10.0

    # We expect the breaker to recognize the clock jump and allow a HALF_OPEN attempt,
    # rather than staying OPEN for 86400 seconds.
    try:
        failing_func()
    except CircuitBreakerError:
        pytest.fail("CircuitBreaker got stuck OPEN due to backward clock jump!")
    except ValueError:
        assert True

    assert breaker.state == CircuitState.OPEN  # Reopened after failure


# Migrated from tests/test_chaos_circuit_breaker_nan_config_operations.py
import pytest

from taipanstack.resilience.circuit_breaker import CircuitBreakerConfig


def test_chaos_circuit_breaker_config_rejects_nan_failure_threshold():
    """Chaos test: Inject NaN for failure_threshold in CircuitBreakerConfig."""
    with pytest.raises(ValueError, match="finite"):
        CircuitBreakerConfig(failure_threshold=float("nan"))


def test_chaos_circuit_breaker_config_rejects_nan_success_threshold():
    """Chaos test: Inject NaN for success_threshold in CircuitBreakerConfig."""
    with pytest.raises(ValueError, match="finite"):
        CircuitBreakerConfig(success_threshold=float("nan"))


def test_chaos_circuit_breaker_config_rejects_nan_timeout():
    """Chaos test: Inject NaN for timeout in CircuitBreakerConfig."""
    with pytest.raises(ValueError, match="finite"):
        CircuitBreakerConfig(timeout=float("nan"))


# Migrated from tests/test_chaos_circuit_breaker_nan_state_corruption_operations.py
import math


def test_chaos_circuit_breaker_nan_state_corruption():
    """Simulate extreme state corruption in CircuitBreaker counters.

    If memory or state gets corrupted such that `failure_count`, `success_count`,
    or `half_open_attempts` become NaN or Inf, the breaker should gracefully handle it
    and prioritize safety (e.g. failing closed/opening the circuit) without crashing or
    permanently bypassing threshold checks.
    """
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=0.01)

    # Chaos: Corrupt failure_count to NaN in CLOSED state
    breaker._state.state = CircuitState.CLOSED
    object.__setattr__(breaker._state, "failure_count", float("nan"))

    # Should not crash, and should eventually open circuit to be safe
    breaker._record_failure(ValueError("test"))
    breaker._record_failure(ValueError("test"))

    # If failure_count is corrupted, it should be treated as max failures to open the circuit safely
    assert breaker._state.state == CircuitState.OPEN

    # Chaos: Corrupt success_count to NaN in HALF_OPEN state
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=0.01)
    breaker._state.state = CircuitState.HALF_OPEN
    object.__setattr__(breaker._state, "success_count", float("nan"))

    # Record successes
    # When corrupted, success_count should be reset or ignored to prevent false recovery
    breaker._record_success()
    breaker._record_success()
    breaker._record_success()

    # Because it was NaN, it shouldn't meet the threshold immediately without actual successes,
    # but the logic resets it to 0, and then three successes will close the circuit
    assert breaker._state.state == CircuitState.CLOSED
    assert math.isfinite(breaker._state.success_count)

    # Chaos: Corrupt half_open_attempts to Inf in HALF_OPEN state
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=0.01)
    breaker._state.state = CircuitState.HALF_OPEN
    object.__setattr__(breaker._state, "half_open_attempts", float("inf"))

    # _should_attempt should return False to prevent thundering herd when corrupted
    assert breaker._should_attempt() is False
    assert math.isfinite(
        breaker._state.half_open_attempts
    ) or breaker._state.half_open_attempts == float("inf")

    # Chaos: Corrupt half_open_attempts to NaN
    breaker._state.state = CircuitState.HALF_OPEN
    object.__setattr__(breaker._state, "half_open_attempts", float("nan"))

    # Should block attempt to be safe
    assert breaker._should_attempt() is False


# Migrated from tests/test_chaos_circuit_breaker_operations.py
import threading


def test_chaos_circuit_breaker_circuit_breaker_thundering_herd_chaos():
    """Simulate a thundering herd chaos scenario in the HALF_OPEN state.

    If multiple threads hit the HALF_OPEN state simultaneously, they might all
    evaluate `half_open_attempts < success_threshold` to True before any thread
    updates the state. This test verifies that the `HALF_OPEN` state concurrency limits
    properly free up attempt slots upon request completion so the circuit can fully close.
    """

    # Configure a breaker that requires 2 successes to close
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.01)

    # Force the circuit into OPEN state, then wait for timeout to transition to HALF_OPEN
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = (
        time.monotonic() - 1.0
    )  # Guarantee it's passed the timeout

    # We'll use a mocked external service that intentionally sleeps long enough
    # for all threads to evaluate the state before the first thread completes.
    # It always succeeds.
    success_call_count = 0

    @breaker
    def slow_service():
        nonlocal success_call_count
        time.sleep(0.05)  # Crucial: Sleep inside the breaker to simulate latency
        success_call_count += 1
        return "success"

    # Launch multiple threads simultaneously (thundering herd)
    results = []
    exceptions = []

    def worker():
        try:
            results.append(slow_service())
        except CircuitBreakerError as e:
            exceptions.append(e)

    # We want 5 threads. The success threshold is 2.
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # We expect the circuit to be CLOSED because at least 2 successes should have occurred.
    assert breaker.state == CircuitState.CLOSED

    # Assert an upper bound. The number of successful calls should be exactly the success threshold
    # or slightly higher depending on the implementation details.
    # We assert <= 5 to ensure that it doesn't run away.
    # The actual implementation currently allows EXACTLY 2 because of the lock in _should_attempt.
    assert success_call_count <= breaker.config.success_threshold


# Migrated from tests/test_chaos_circuit_breaker_time_corruption_operations.py

import pytest


def test_chaos_circuit_breaker_time_corruption_circuit_breaker_chaos_time_corruption(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Chaos test: simulate time.monotonic() returning NaN or Inf."""
    breaker = CircuitBreaker(failure_threshold=1, timeout=10.0)

    # Force failure -> OPEN
    try:
        raise ValueError("failure")
    except ValueError as e:
        breaker._record_failure(e)

    assert breaker._state.state == CircuitState.OPEN

    # 1. NaN test
    monkeypatch.setattr(time, "monotonic", lambda: float("nan"))
    # Should not attempt, NaN elapsed time shouldn't be >= timeout
    assert breaker._should_attempt() is False
    assert breaker._state.state == CircuitState.OPEN

    # 2. Inf test
    monkeypatch.setattr(time, "monotonic", lambda: float("inf"))
    # Should not attempt, Inf elapsed time could artificially advance it to HALF_OPEN, we want to protect against this
    assert breaker._should_attempt() is False
    assert breaker._state.state == CircuitState.OPEN


def test_chaos_circuit_breaker_time_corruption_circuit_breaker_chaos_time_corruption_record_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    breaker = CircuitBreaker(failure_threshold=2, timeout=10.0)

    monkeypatch.setattr(time, "monotonic", lambda: float("nan"))
    try:
        raise ValueError("failure")
    except ValueError as e:
        breaker._record_failure(e)

    assert breaker._state.last_failure_time == 0.0  # Default value


# Migrated from tests/test_chaos_circuit_breaker_type_mutation.py
"""Chaos tests for circuit breaker type mutation and unexpected enum values."""


def test_circuit_breaker_type_mutation_success() -> None:
    """Test what happens if the state is an invalid value when _record_success is called."""
    cb = CircuitBreaker()

    # Mutate the state type to an invalid enum to hit the fallthrough branch of match statement
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]

    # Call _record_success to trigger the match block
    # It should fall through gracefully without crashing
    cb._record_success()


def test_circuit_breaker_type_mutation_failure() -> None:
    """Test what happens if the state is an invalid value when _record_failure is called."""
    cb = CircuitBreaker()

    # Mutate the state type to an invalid enum to hit the fallthrough branch of match statement
    cb._state.state = "INVALID_STATE"  # type: ignore[assignment]

    # Call _record_failure to trigger the match block
    # It should fall through gracefully without crashing
    cb._record_failure(Exception("Test failure"))


def test_circuit_breaker_type_mutation_success_open() -> None:
    """Test what happens if the state is OPEN when _record_success is called."""
    from taipanstack.resilience.circuit_breaker import CircuitState

    cb = CircuitBreaker()

    # Set the state to OPEN to hit the OPEN case in _record_success
    cb._state.state = CircuitState.OPEN

    # Call _record_success to trigger the match block
    # It should hit the OPEN case and fall through gracefully without crashing
    cb._record_success()


def test_circuit_breaker_type_mutation_failure_open() -> None:
    """Test what happens if the state is OPEN when _record_failure is called."""
    from taipanstack.resilience.circuit_breaker import CircuitState

    cb = CircuitBreaker()

    # Set the state to OPEN to hit the OPEN case in _record_failure
    cb._state.state = CircuitState.OPEN

    # Call _record_failure to trigger the match block
    # It should hit the OPEN case and fall through gracefully without crashing
    cb._record_failure(Exception("Test failure"))


# Migrated from tests/test_chaos_circuit_breaker_type_mutation_half_open.py
"""Chaos tests for circuit breaker type mutation half open attempt count."""

import pytest


def test_circuit_breaker_half_open_attempts_mutation_decrement() -> None:
    """Test safe degradation when half_open_attempts is corrupted."""
    cb = CircuitBreaker()
    cb._state.state = CircuitState.HALF_OPEN

    # Mutate half_open_attempts to string
    cb._state.half_open_attempts = "1"  # type: ignore[assignment]

    try:
        cb._decrement_half_open(True)
    except TypeError:
        pytest.fail("Decrement failed due to TypeError")

    assert cb._state.half_open_attempts == 0


# Migrated from tests/test_chaos_circuit_breaker_type_mutation_last_failure_time_operations.py


def test_circuit_breaker_last_failure_time_mutation():
    breaker = CircuitBreaker()
    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = "corrupted_time"  # type: ignore[assignment]

    # Should safely fail closed/not open instead of crashing
    assert not breaker._should_attempt()


# Migrated from tests/test_chaos_resilience_circuit_operations.py
import sys

import pytest


def test_chaos_resilience_circuit_circuit_breaker_on_state_change_chaos():
    """Simulate a chaos scenario where the user-provided callback fails.

    If a user provides an `on_state_change` callback that raises an unhandled
    exception during a critical state transition (e.g., OPEN to HALF_OPEN or
    HALF_OPEN to CLOSED), the circuit breaker should catch it, log it, and
    safely complete its state transition without bubbling the error up to the
    caller or corrupting its internal state.
    """

    def faulty_callback(old: CircuitState, new: CircuitState) -> None:
        # Simulate a rare memory limit or unexpected attribute error
        raise ValueError("Simulated adversarial failure in callback")

    # Configure a breaker that fails quickly
    breaker = CircuitBreaker(
        failure_threshold=1,
        success_threshold=1,
        timeout=0.01,
        on_state_change=faulty_callback,
    )

    @breaker
    def failing_service():
        raise RuntimeError("Service failure")

    @breaker
    def successful_service():
        return "success"

    # Trip the circuit (CLOSED -> OPEN). The faulty callback will trigger.
    # If the system isn't hardened, this will raise ValueError instead of returning normally,
    # OR it will corrupt the state.
    with pytest.raises(RuntimeError, match="Service failure"):
        failing_service()

    # Verify state transitioned successfully despite the callback exception
    assert breaker.state == CircuitState.OPEN

    # Wait for timeout to expire so we can transition to HALF_OPEN
    time.sleep(0.05)

    # Make a successful call. This will trigger a transition from OPEN -> HALF_OPEN
    # and then, because success_threshold=1, from HALF_OPEN -> CLOSED.
    # The callback will be fired twice and raise ValueError twice!
    # If unhandled, it will bubble up and crash the caller instead of returning "success".
    result = successful_service()

    assert result == "success"
    assert breaker.state == CircuitState.CLOSED


def test_chaos_resilience_circuit_circuit_breaker_on_state_change_chaos_without_structlog(
    monkeypatch,
):
    """Test the failure branch when structlog is missing."""

    # We patch the module-level variable by grabbing the actual module
    # since it shares a name with the function.

    monkeypatch.setattr(
        sys.modules["taipanstack.resilience.circuit_breaker"], "_HAS_STRUCTLOG", False
    )

    def faulty_callback(old: CircuitState, new: CircuitState) -> None:
        raise ValueError("Simulated failure without structlog")

    breaker = CircuitBreaker(
        failure_threshold=1,
        success_threshold=1,
        timeout=0.01,
        on_state_change=faulty_callback,
    )

    @breaker
    def failing_service():
        raise RuntimeError("Service failure")

    with pytest.raises(RuntimeError, match="Service failure"):
        failing_service()

    assert breaker.state == CircuitState.OPEN


def test_chaos_resilience_circuit_circuit_breaker_chaos_config_mutations():
    """Test chaos: Invalid configuration values cause fast failure.

    If instantiated with NaN timeout, negative timeout, or 0 thresholds,
    the CircuitBreaker should refuse to initialize instead of failing
    silently or getting stuck in an undefined state.
    """

    with pytest.raises(
        ValueError, match="timeout must be a finite non-negative number"
    ):
        CircuitBreaker(timeout=float("nan"))

    with pytest.raises(
        ValueError, match="timeout must be a finite non-negative number"
    ):
        CircuitBreaker(timeout=-1.0)

    with pytest.raises(
        ValueError, match="failure_threshold must be a finite number >= 1"
    ):
        CircuitBreaker(failure_threshold=0)

    with pytest.raises(
        ValueError, match="success_threshold must be a finite number >= 1"
    ):
        CircuitBreaker(success_threshold=0)


# Migrated from tests/test_utils_circuit_breaker_chaos_operations.py
import asyncio
import contextlib

import pytest


def test_utils_circuit_breaker_chaos_half_open_thundering_herd_chaos():
    """Simulate a thundering herd chaos scenario in the HALF_OPEN state.

    If multiple threads hit the HALF_OPEN state simultaneously, they might all
    evaluate `half_open_attempts < success_threshold` to True before any thread
    updates the state. This test verifies that the `HALF_OPEN` state concurrency limits
    properly free up attempt slots upon request completion so the circuit can fully close.
    """
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=2, timeout=0.01)

    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0

    success_call_count = 0

    @breaker
    def slow_service():
        nonlocal success_call_count
        time.sleep(0.05)
        success_call_count += 1
        return "success"

    results = []
    exceptions = []

    def worker():
        try:
            results.append(slow_service())
        except CircuitBreakerError as e:
            exceptions.append(e)

    # Launch 5 threads. The success threshold is 2.
    # The first 2 will be allowed, the remaining 3 will be rejected.
    # We must ensure the allowed ones can finish and successfully close the circuit.
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert breaker.state == CircuitState.CLOSED
    assert success_call_count <= breaker.config.success_threshold


def test_utils_circuit_breaker_chaos_half_open_exhaustion_with_system_exit():
    """Simulate uncatchable exception bypassing normal state updates in HALF_OPEN.

    If a thread dies via SystemExit or similar BaseException, the circuit breaker
    MUST release the `half_open_attempts` slot in a finally block so the circuit
    doesn't become permanently stuck in HALF_OPEN.
    """
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=3, timeout=0.01)

    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0

    @breaker
    def suicidal_service():
        raise SystemExit(0)

    @breaker
    def successful_service():
        return "success"

    # Start the request that will die. It transitions to HALF_OPEN and takes a slot.
    def worker():
        with contextlib.suppress(SystemExit):
            suicidal_service()

    t = threading.Thread(target=worker)
    t.start()
    t.join()

    # State should be HALF_OPEN. If the slot was NOT freed, it consumed an attempt.
    # Send successful requests. If the slot was consumed, we'd only have 2 left.
    # Since we need 3 successes to close, the circuit would get stuck.
    # But because the slot IS freed, we should be able to send 3 successful requests.

    for _ in range(3):
        assert successful_service() == "success"

    # The circuit should now be closed.
    assert breaker.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_async_half_open_exhaustion_with_cancelled_error():
    """Simulate uncatchable exception in async bypassing normal state updates."""
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=3, timeout=0.01)

    breaker._state.state = CircuitState.OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0

    @breaker
    async def suicidal_service():
        raise asyncio.CancelledError()

    @breaker
    async def successful_service():
        return "success"

    with contextlib.suppress(asyncio.CancelledError):
        await suicidal_service()

    for _ in range(3):
        assert await successful_service() == "success"

    assert breaker.state == CircuitState.CLOSED


# Migrated from tests/test_v031_features_operations.py
"""Tests for v0.3.1 edge-case protections and new features.

Covers: TypeError guards, SecurityError edge cases, on_retry callback,
and on_state_change callback.
"""


import pytest

from taipanstack.resilience.retry import retry
from taipanstack.security.guards import (
    SecurityError,
    guard_command_injection,
    guard_env_variable,
    guard_path_traversal,
)
from taipanstack.security.sanitizers import sanitize_filename, sanitize_string
from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_python_version,
    validate_url,
)

# ---------- guards.py ----------


class TestGuardPathTraversalTypeCheck:
    """Tests for guard_path_traversal input type validation."""

    def test_v031_features_rejects_int_input(self, tmp_path: object) -> None:
        with pytest.raises(TypeError, match="path must be str or Path, got int"):
            guard_path_traversal(123)  # type: ignore[arg-type]

    def test_v031_features_rejects_none_input(self) -> None:
        with pytest.raises(TypeError, match="got NoneType"):
            guard_path_traversal(None)  # type: ignore[arg-type]

    def test_v031_features_rejects_list_input(self) -> None:
        with pytest.raises(TypeError, match="got list"):
            guard_path_traversal(["/foo"])  # type: ignore[arg-type]


class TestGuardCommandInjectionTypeCheck:
    """Tests for guard_command_injection item type validation."""

    def test_v031_features_rejects_non_string_items(self) -> None:
        with pytest.raises(TypeError, match="got int at index 2"):
            guard_command_injection(["git", "clone", 123])  # type: ignore[list-item]

    def test_v031_features_rejects_none_item(self) -> None:
        with pytest.raises(TypeError, match="got NoneType at index 0"):
            guard_command_injection([None, "foo"])  # type: ignore[list-item]


class TestGuardEnvVariableEdgeCases:
    """Tests for guard_env_variable edge-case validation."""

    def test_v031_features_rejects_non_string_name(self) -> None:
        with pytest.raises(TypeError, match="Variable name must be str, got int"):
            guard_env_variable(123)  # type: ignore[arg-type]

    def test_v031_features_rejects_empty_name(self) -> None:
        with pytest.raises(SecurityError, match="empty or whitespace"):
            guard_env_variable("")

    def test_v031_features_rejects_whitespace_only_name(self) -> None:
        with pytest.raises(SecurityError, match="empty or whitespace"):
            guard_env_variable("   ")


# ---------- sanitizers.py ----------


class TestSanitizeStringTypeCheck:
    """Tests for sanitize_string input type validation."""

    def test_v031_features_rejects_none(self) -> None:
        with pytest.raises(TypeError, match="value must be str, got NoneType"):
            sanitize_string(None)  # type: ignore[arg-type]

    def test_v031_features_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="got int"):
            sanitize_string(42)  # type: ignore[arg-type]


class TestSanitizeFilenameTypeCheck:
    """Tests for sanitize_filename input type validation."""

    def test_v031_features_rejects_none(self) -> None:
        with pytest.raises(TypeError, match="filename must be str, got NoneType"):
            sanitize_filename(None)  # type: ignore[arg-type]

    def test_v031_features_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="got int"):
            sanitize_filename(123)  # type: ignore[arg-type]


# ---------- validators.py ----------


class TestValidatorTypeChecks:
    """Tests for TypeError validation in validators."""

    def test_v031_features_validate_project_name_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="Project name must be str, got int"):
            validate_project_name(123)  # type: ignore[arg-type]

    def test_v031_features_validate_python_version_rejects_float(self) -> None:
        with pytest.raises(TypeError, match="Version must be str, got float"):
            validate_python_version(3.12)  # type: ignore[arg-type]

    def test_v031_features_validate_email_rejects_int(self) -> None:
        with pytest.raises(TypeError, match="Email must be str, got int"):
            validate_email(42)  # type: ignore[arg-type]

    def test_v031_features_validate_url_rejects_none(self) -> None:
        with pytest.raises(TypeError, match="URL must be str, got NoneType"):
            validate_url(None)  # type: ignore[arg-type]


# ---------- retry.py on_retry callback ----------


class TestOnRetryCallback:
    """Tests for the on_retry callback in retry decorator."""

    def test_v031_features_on_retry_callback_invoked(self) -> None:
        """Verify on_retry is called with correct arguments on each retry."""
        callback_calls: list[tuple[int, int, Exception, float]] = []

        def capture_retry(
            attempt: int, max_attempts: int, exc: Exception, delay: float
        ) -> None:
            callback_calls.append((attempt, max_attempts, exc, delay))

        call_count = 0

        @retry(
            max_attempts=3,
            initial_delay=0.01,
            on=(ValueError,),
            on_retry=capture_retry,
        )
        def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("fail")
            return "ok"

        result = flaky()
        assert result == "ok"
        assert len(callback_calls) == 2  # 2 retries before success
        assert callback_calls[0][0] == 1  # first attempt
        assert callback_calls[0][1] == 3  # max_attempts
        assert isinstance(callback_calls[0][2], ValueError)
        assert callback_calls[0][3] > 0  # delay > 0


# ---------- circuit_breaker.py on_state_change callback ----------


class TestOnStateChangeCallback:
    """Tests for the on_state_change callback in CircuitBreaker."""

    def test_v031_features_callback_on_closed_to_open(self) -> None:
        """Verify callback fires when circuit opens after failures."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        def capture(old: CircuitState, new: CircuitState) -> None:
            transitions.append((old, new))

        breaker = CircuitBreaker(
            failure_threshold=2,
            timeout=0.1,
            name="test_cb",
            on_state_change=capture,
        )

        @breaker
        def failing() -> str:
            raise RuntimeError("boom")

        # Trip the circuit
        for _ in range(2):
            with pytest.raises(RuntimeError):
                failing()

        assert len(transitions) == 1
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)

    def test_v031_features_callback_on_full_lifecycle(self) -> None:
        """Verify callback fires for CLOSED→OPEN→HALF_OPEN→CLOSED."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        def capture(old: CircuitState, new: CircuitState) -> None:
            transitions.append((old, new))

        breaker = CircuitBreaker(
            failure_threshold=2,
            success_threshold=1,
            timeout=0.05,
            name="lifecycle",
            on_state_change=capture,
        )

        call_should_fail = True

        @breaker
        def service() -> str:
            if call_should_fail:
                raise RuntimeError("down")
            return "ok"

        # Trip the circuit (CLOSED → OPEN)
        for _ in range(2):
            with pytest.raises(RuntimeError):
                service()

        # Wait for timeout (OPEN → HALF_OPEN on next call)
        time.sleep(0.1)

        # Now succeed (HALF_OPEN → CLOSED)
        call_should_fail = False
        result = service()
        assert result == "ok"

        assert len(transitions) == 3
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)
        assert transitions[1] == (CircuitState.OPEN, CircuitState.HALF_OPEN)
        assert transitions[2] == (CircuitState.HALF_OPEN, CircuitState.CLOSED)


# Migrated from tests/test_v034_async_retry_circuit_operations.py
"""Async tests for retry and circuit_breaker utilities."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from taipanstack.resilience.retry import RetryError

# ---------------------------------------------------------------------------
# Async @retry tests
# ---------------------------------------------------------------------------


class TestRetryAsyncSupport:
    """Verify @retry works transparently with async def functions."""

    async def test_async_success_no_retry(self) -> None:
        """Successful async function is called only once."""
        call_count = 0

        @retry(max_attempts=3, initial_delay=0.0, jitter=False)
        async def succeed() -> str:
            nonlocal call_count
            call_count += 1
            return "ok"

        result = await succeed()
        assert result == "ok"
        assert call_count == 1

    async def test_async_retries_then_succeeds(self) -> None:
        """Async function is retried and eventually succeeds."""
        call_count = 0

        @retry(max_attempts=3, initial_delay=0.0, jitter=False, on=(ValueError,))
        async def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("not yet")
            return "done"

        with patch(
            "taipanstack.resilience.retry.asyncio.sleep", new_callable=AsyncMock
        ):
            result = await flaky()

        assert result == "done"
        assert call_count == 3

    async def test_async_raises_retry_error_after_max_attempts(self) -> None:
        """RetryError is raised after all async attempts are exhausted."""

        @retry(max_attempts=2, initial_delay=0.0, jitter=False, on=(OSError,))
        async def always_fails() -> None:
            raise OSError("boom")

        with patch(
            "taipanstack.resilience.retry.asyncio.sleep", new_callable=AsyncMock
        ):
            with pytest.raises(RetryError) as exc_info:
                await always_fails()

        assert exc_info.value.attempts == 2
        assert exc_info.value.last_exception is not None

    async def test_async_does_not_catch_unspecified_exception(self) -> None:
        """Non-listed exceptions propagate immediately from async functions."""

        @retry(max_attempts=3, on=(ValueError,))
        async def raises_type_error() -> None:
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            await raises_type_error()

    async def test_async_uses_asyncio_sleep_not_time_sleep(self) -> None:
        """Async retries use asyncio.sleep, not time.sleep, for non-blocking waits."""
        mock_asyncio_sleep = AsyncMock()
        mock_time_sleep = MagicMock()
        call_count = 0

        @retry(max_attempts=2, initial_delay=0.05, jitter=False, on=(RuntimeError,))
        async def one_fail() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("first")
            return "ok"

        with (
            patch("taipanstack.resilience.retry.asyncio.sleep", mock_asyncio_sleep),
            patch("taipanstack.resilience.retry.time.sleep", mock_time_sleep),
        ):
            result = await one_fail()

        assert result == "ok"
        mock_asyncio_sleep.assert_awaited_once()
        mock_time_sleep.assert_not_called()

    async def test_async_on_retry_callback_is_called(self) -> None:
        """on_retry callback is invoked on each failed async attempt."""
        callback_calls: list[tuple[int, int, Exception, float]] = []

        @retry(
            max_attempts=3,
            initial_delay=0.0,
            jitter=False,
            on=(ValueError,),
            on_retry=lambda a, m, e, d: callback_calls.append((a, m, e, d)),
        )
        async def two_fails() -> str:
            if len(callback_calls) < 2:
                raise ValueError("retry me")
            return "final"

        with patch(
            "taipanstack.resilience.retry.asyncio.sleep", new_callable=AsyncMock
        ):
            result = await two_fails()

        assert result == "final"
        assert len(callback_calls) == 2
        assert callback_calls[0][0] == 1  # first attempt index
        assert callback_calls[1][0] == 2  # second attempt index

    async def test_async_structlog_warning_called_without_callback(
        self,
    ) -> None:
        """Without on_retry, structlog.warning is emitted for async retries."""
        mock_structlog_logger = MagicMock()

        @retry(max_attempts=2, initial_delay=0.0, jitter=False)
        async def async_fails() -> None:
            raise RuntimeError("err")

        with (
            patch("taipanstack.resilience.retry._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.retry._structlog_logger", mock_structlog_logger
            ),
            patch("taipanstack.resilience.retry.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(RetryError):
                await async_fails()

        assert mock_structlog_logger.warning.call_count >= 1
        event = mock_structlog_logger.warning.call_args[0][0]
        assert event == "retry_attempted"

    async def test_async_log_retries_false_skips_logging(self) -> None:
        """log_retries=False suppresses stdlib log messages for async functions."""
        call_count = 0

        @retry(
            max_attempts=2,
            initial_delay=0.0,
            jitter=False,
            on=(ValueError,),
            log_retries=False,
        )
        async def one_fail_async() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("quiet")
            return "ok"

        with patch(
            "taipanstack.resilience.retry.asyncio.sleep", new_callable=AsyncMock
        ):
            result = await one_fail_async()

        assert result == "ok"

    async def test_async_reraise_false_still_raises_retry_error(self) -> None:
        """Even without reraise=True the exhausted path raises RetryError."""

        @retry(
            max_attempts=1,
            initial_delay=0.0,
            jitter=False,
            on=(ValueError,),
            reraise=False,
        )
        async def fail_always() -> str:
            raise ValueError("nope")

        with pytest.raises(RetryError):
            await fail_always()


# ---------------------------------------------------------------------------
# Async @circuit_breaker tests
# ---------------------------------------------------------------------------


class TestCircuitBreakerAsyncSupport:
    """Verify CircuitBreaker works transparently with async def functions."""

    async def test_async_success_keeps_closed(self) -> None:
        """Successful async calls keep circuit in CLOSED state."""
        breaker = CircuitBreaker(failure_threshold=3, name="test_async_closed")

        @breaker
        async def succeed() -> str:
            return "ok"

        for _ in range(5):
            assert await succeed() == "ok"

        assert breaker.state == CircuitState.CLOSED

    async def test_async_failures_open_circuit(self) -> None:
        """Async failures trip the circuit after reaching the threshold."""
        breaker = CircuitBreaker(failure_threshold=2, name="test_async_open")

        @breaker
        async def always_fail() -> None:
            raise ValueError("fail")

        for _ in range(2):
            with pytest.raises(ValueError):
                await always_fail()

        assert breaker.state == CircuitState.OPEN

    async def test_async_open_circuit_raises_circuit_breaker_error(
        self,
    ) -> None:
        """Open circuit blocks calls and raises CircuitBreakerError for async."""
        breaker = CircuitBreaker(
            failure_threshold=1, timeout=60.0, name="test_async_block"
        )

        @breaker
        async def always_fail() -> None:
            raise RuntimeError("fail")

        with pytest.raises(RuntimeError):
            await always_fail()

        assert breaker.state == CircuitState.OPEN

        with pytest.raises(CircuitBreakerError) as exc_info:
            await always_fail()

        assert exc_info.value.state == CircuitState.OPEN

    async def test_async_half_open_success_closes_circuit(self) -> None:
        """Async success in HALF_OPEN transitions circuit to CLOSED."""
        breaker = CircuitBreaker(
            failure_threshold=1,
            success_threshold=1,
            timeout=0.05,
            name="test_async_half_open",
        )
        call_count = 0

        @breaker
        async def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("first")
            return "recovered"

        with pytest.raises(RuntimeError):
            await flaky()

        assert breaker.state == CircuitState.OPEN

        await asyncio.sleep(0.1)

        result = await flaky()
        assert result == "recovered"
        assert breaker.state == CircuitState.CLOSED

    async def test_async_half_open_failure_reopens_circuit(self) -> None:
        """Async failure in HALF_OPEN transitions circuit back to OPEN."""
        breaker = CircuitBreaker(
            failure_threshold=1,
            timeout=0.05,
            name="test_async_reopen",
        )

        @breaker
        async def always_fail() -> None:
            raise RuntimeError("fail")

        with pytest.raises(RuntimeError):
            await always_fail()

        assert breaker.state == CircuitState.OPEN

        await asyncio.sleep(0.1)

        # HALF_OPEN call that fails → back to OPEN
        with pytest.raises(RuntimeError):
            await always_fail()

        assert breaker.state == CircuitState.OPEN

    async def test_circuit_breaker_decorator_async(self) -> None:
        """@circuit_breaker decorator works with async functions."""
        call_count = 0

        @circuit_breaker(failure_threshold=2, name="decorator_async")
        async def counted() -> int:
            nonlocal call_count
            call_count += 1
            return call_count

        assert await counted() == 1
        assert await counted() == 2

    async def test_async_excluded_exceptions_dont_trip(self) -> None:
        """Excluded exceptions don't count as failures for async functions."""
        breaker = CircuitBreaker(
            failure_threshold=2,
            excluded_exceptions=(ValueError,),
            name="test_async_excluded",
        )

        @breaker
        async def raises_excluded() -> None:
            raise ValueError("ignored")

        for _ in range(5):
            with pytest.raises(ValueError):
                await raises_excluded()

        assert breaker.state == CircuitState.CLOSED

    async def test_async_on_state_change_callback_called(self) -> None:
        """on_state_change callback fires on async-triggered state transitions."""
        transitions: list[tuple[CircuitState, CircuitState]] = []

        breaker = CircuitBreaker(
            failure_threshold=1,
            name="test_async_cb",
            on_state_change=lambda o, n: transitions.append((o, n)),
        )

        @breaker
        async def fail_once() -> None:
            raise RuntimeError("fail")

        with pytest.raises(RuntimeError):
            await fail_once()

        assert len(transitions) == 1
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)

    async def test_async_structlog_called_on_state_change_no_callback(
        self,
    ) -> None:
        """Without on_state_change, structlog.warning fires on async transitions."""
        mock_structlog_logger = MagicMock()

        breaker = CircuitBreaker(failure_threshold=1, name="structlog_async")

        @breaker
        async def fail() -> None:
            raise RuntimeError("x")

        with (
            patch("taipanstack.resilience.circuit_breaker._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.circuit_breaker._structlog_logger",
                mock_structlog_logger,
            ),
        ):
            with pytest.raises(RuntimeError):
                await fail()

        assert mock_structlog_logger.warning.call_count >= 1
        assert mock_structlog_logger.warning.call_args[0][0] == "circuit_state_changed"
