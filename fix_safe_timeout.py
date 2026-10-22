import sys

def modify_circuit_breaker():
    with open('src/taipanstack/resilience/circuit_breaker.py', 'r') as f:
        content = f.read()

    new_content = content.replace(
        "            return self._get_safe_timeout()",
        "            return self._get_safe_threshold(self.config.timeout, 0, 30.0)"
    )
    with open('src/taipanstack/resilience/circuit_breaker.py', 'w') as f:
        f.write(new_content)

def modify_time_corruption():
    with open('tests/test_chaos_circuit_breaker_time_corruption.py', 'r') as f:
        content = f.read()

    new_content = content.replace(
        """    assert breaker._state.state == CircuitState.HALF_OPEN
    # Also adjust the NaN check because wait, it failed in the NaN check
    """,
        """    assert breaker._state.state == CircuitState.HALF_OPEN"""
    )
    with open('tests/test_chaos_circuit_breaker_time_corruption.py', 'w') as f:
        f.write(new_content)

modify_circuit_breaker()
modify_time_corruption()
