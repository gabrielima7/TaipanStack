## Complexity Reduction and Technical Debt Refactoring

**Modules Refactored:**
- `src/taipanstack/resilience/watchdogs/health_pinger.py`

**Functions Refactored:**
- `HealthPinger._update_target_status`

**Architectural Strategies Used:**
- Extracted logic for checking and force-opening the circuit breaker into a dedicated helper method `_check_and_open_breaker`.
- Extracted logic for notifying health changes and logging into a dedicated helper method `_notify_health_change`.
- Maintained guard clauses and early returns within the main `_update_target_status` method to keep nesting low.
- Maintained exact logic, side-effects, type annotations, and the exact same public API.

**Complexity Reduction Metrics:**
- **Before:** `HealthPinger._update_target_status` had a cyclomatic complexity of **B (7)**.
- **After:** The logic is now split across `_update_target_status`, `_check_and_open_breaker`, and `_notify_health_change`, bringing the maximum cyclomatic complexity in `HealthPinger` down to **A (4)**. The average complexity for the file dropped to **A (2.54)**.
