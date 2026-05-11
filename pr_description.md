### Professional Complexity Reduction and Technical Debt Refactoring

This Pull Request introduces significant reductions in cyclomatic complexity across three critical modules in the TaipanStack project. The objective is to adhere strictly to Clean Code and SOLID principles while maintaining 100% test coverage and guaranteeing identical public API behavior.

#### Modules and Functions Refactored:
1. `src/taipanstack/resilience/retry.py`: Refactored `RetryConfig.__post_init__` to extract validation logic.
2. `src/taipanstack/resilience/circuit_breaker.py`: Refactored `CircuitBreaker._decrement_half_open` to reduce deep nesting.
3. `src/taipanstack/resilience/adaptive/orchestrator.py`: Refactored `ResilienceOrchestrator._execute_with_retries` to replace structural pattern matching with `isinstance` checks.

#### Architectural Strategies Used:
- **Extracted validation logic into a dedicated helper:** In `RetryConfig`, the redundant `math.isfinite` validation across five fields was extracted into the private `_validate_finite` method, drastically reducing the cyclomatic complexity of `__post_init__` from B to A level.
- **Applied guard clauses to reduce nesting:** In `CircuitBreaker._decrement_half_open`, multiple layers of nested `if` statements were replaced with early returns, flattening the control flow and improving readability without altering the `TypeError` handling required for state corruption.
- **Enhanced static typing and simplified control flow:** In `ResilienceOrchestrator._execute_with_retries`, a `match/case` block was replaced with explicit `isinstance(result, (Ok, Err))` checks, satisfying strict mypy requirements and reducing overall branching complexity.

#### Complexity Reduction Metrics:
- Cyclomatic complexity for all refactored methods now falls comfortably within the `A` tier.
- Nesting levels have been reduced, and redundant code has been consolidated, satisfying DRY principles.
