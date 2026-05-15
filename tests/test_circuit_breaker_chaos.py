import time

import pytest

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)


def test_chaos_circuit_breaker_config_mutation_resilience():
    # Initialize a breaker with standard config
    breaker = CircuitBreaker(failure_threshold=1, timeout=0.1)

    # Force open state
    try:

        @breaker
        def fail_always():
            raise RuntimeError("Chaos Error")

        fail_always()
    except RuntimeError:
        pass

    assert breaker.state == CircuitState.OPEN

    # Chaos Injection: Mutate the config timeout maliciously to a string
    try:
        breaker.config.timeout = "corrupted"  # type: ignore
    except Exception as e:
        # If the object is frozen or throws, the chaos injection failed (which means resilience is active!)
        _ = e  # Prevent unused variable warning

    # Wait for what would be the timeout period
    time.sleep(0.2)

    # Attempt to call. If the system is vulnerable, this will raise a TypeError inside the circuit breaker
    # when comparing `elapsed >= self.config.timeout`
    try:

        @breaker
        def succeed():
            return True

        succeed()
    except TypeError as e:
        pytest.fail(
            f"VULNERABILITY: Circuit breaker crashed due to config corruption: {e}"
        )
    except CircuitBreakerError:
        # If it's still open, that's fine. It shouldn't crash.
        pass
    except RuntimeError:
        # In case our function throws
        pass
