This pull request implements rigorous micro-chaos experiments targeting the `taipanstack.utils.rate_limit` module, ensuring its behavior under severe internal corruption and extreme states.

Actions taken:
*   Authored comprehensive chaos tests in `tests/test_chaos_rate_limit_resilience.py` to target state corruption (e.g. `NaN`/`Inf` properties, backward time jumps, variable type mutations) in the rate limiter logic.
*   Refactored the core logic in `src/taipanstack/utils/rate_limit.py` to cleanly remove unreachable and overly defensive error branches (specifically exception handling that was entirely masked by the resilient `consume` method), prioritizing a safe fail-closed mechanism over risky self-healing logic when state invariants are broken.
*   Achieved and validated absolute 100% test line and branch coverage across the repository using `pytest`.
*   Successfully ran static analysis tools (`ruff` and `mypy`) locally, ensuring no regressions.
