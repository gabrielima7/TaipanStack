# Description

This pull request addresses coverage gaps in the TaipanStack core resilience module, specifically hitting the uncovered implicit `->exit` branch and implicit match `CircuitState.OPEN` statement.

## Edge cases handled
- Covered the missing `CircuitState.OPEN` branch in `_record_success` of `CircuitBreaker`.
- Covered the missing `CircuitState.OPEN` branch in `_record_failure` of `CircuitBreaker`.
- Hit the implicit `->exit` fallthrough block in match statements by testing invalid state enums correctly hitting the final `pass` branch.

## Files Modified
- `tests/test_chaos_circuit_breaker_type_mutation.py` (New tests added)

## Metrics
- Overall branch coverage successfully improved back to 100%.
