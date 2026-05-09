### Micro-Chaos Experiment: CircuitBreaker state type corruption

**Component Targeted:**
- `src/taipanstack/resilience/circuit_breaker.py` (`_decrement_half_open` method)

**Simulated Failure:**
- Executed a micro-chaos experiment targeting internal state variables, specifically `half_open_attempts`. The test deliberately assigns an incorrect type (a string `"1"` instead of an integer) to `self._state.half_open_attempts` while the circuit is in the `HALF_OPEN` state to verify behavior during concurrent operations or memory corruption.

**Code Adjustments:**
- The original code checked `self._state.half_open_attempts > 0`, which raised a `TypeError` and crashed the program when mutated to a string.
- Refactored `_decrement_half_open` to place the logical check within a `try...except TypeError` block.
- Implemented `math.isfinite(self._state.half_open_attempts)` as a protective type and bound-checking guard before executing the decrement.
- The circuit breaker now gracefully intercepts the `TypeError` and defaults the internal `half_open_attempts` value to 0, ensuring safe degradation and recovery rather than catastrophic system failure.
