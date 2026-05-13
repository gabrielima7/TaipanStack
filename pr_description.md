# Refactor: Reduce Cyclomatic Complexity in Resilience Modules

## Overview
This PR focuses on analyzing and reducing cyclomatic complexity across the `src/taipanstack/resilience/` directory, adhering strictly to Clean Code and SOLID principles.

## Modules Refactored
- `src/taipanstack/resilience/retry.py`
- `src/taipanstack/resilience/circuit_breaker.py`
- `src/taipanstack/resilience/adaptive/orchestrator.py`

## Architectural Strategies Used
- **Extracted Private Helper Methods:** Deep nesting and complex boolean logic were refactored into smaller, testable, and well-named helper methods. Examples include `_calculate_jitter_offset` in `retry.py` and `_get_failure_state_change` in `circuit_breaker.py`.
- **Early Returns and Guard Clauses:** Simplified complex logic blocks (e.g., in `Retrier.__exit__`) by handling failure cases early and returning, reducing overall nesting.
- **Replaced Structural Pattern Matching with Explicit If/Elif:** Converted `match`/`case` blocks to explicit type guarding (`if isinstance`) and explicit `if/elif` state checks in the circuit breaker and orchestrator modules. This ensures better static typing (mypy narrowing) and complies with the project's strict guidelines.

## Complexity Reduction
- Complexity in `Retrier.__exit__`, `_apply_jitter`, `_record_failure`, `_decrement_half_open` and `_execute_with_retries` has been significantly reduced (all from 'B' grade to 'A' grade complexity), ensuring these methods are cleaner, easier to maintain, and strictly typed.
