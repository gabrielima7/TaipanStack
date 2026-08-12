**Security Hardening & Fuzzing: Micro-Chaos Testing for RateLimiter Resilience**

## Objective
Proactively harden the TaipanStack project by performing a daily "micro-chaos" experiment on its resilience mechanisms, focusing specifically on `RateLimiter` in `src/taipanstack/utils/rate_limit.py`.

## Component Targeted
- `RateLimiter`
- `@rate_limit` (sync and async decorator wrappers)
- Internal token bucket mechanism (`_apply_new_tokens`, `_try_consume`, `_add_tokens`)

## Malformed Property Data Generated (Chaos Injection)
- **Lock Mutations:** Replaced internal threading locks with objects that raise `RuntimeError` on `acquire()`.
- **State Corruption:** Mutated internal float state variables (`tokens`, `last_update`, `capacity`, `time_window`) to `None`, `invalid_string`, and `float("inf")`.
- **Exception Simulation:** Patched `time.monotonic` to raise `Exception` simulating clock failures.
- **Malformed Inputs:** Passed invalid bounds (`None`, `inf`, negative numbers, strings) to internal token bucket algorithms.

## Verification and Code Adjustments
The existing source code in `rate_limit.py` was thoroughly verified and proven to degrade safely during all the above failure modes. No production crashes occurred. The `RateLimiter` correctly fell back to returning `False` or capping corrupted state values back to safe capacities without raising raw exceptions. A broad `try/except` block covering lock acquisition is now fully backed by these explicit lock mutation tests, maintaining TaipanStack's strict 100% real branch coverage requirement.
