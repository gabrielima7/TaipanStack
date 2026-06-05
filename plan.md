1. **Fix missing `isinstance` checks before `math.isfinite`**
   - Apply fixes to `subprocess.py`, `rate_limit.py`, `decorators.py`, `bulkhead.py`, `orchestrator.py`, and `circuit_breaker.py` by replacing incorrect conditionals with proper `isinstance` checks using a python script. This was verified to work correctly.

2. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**
   - Run `pre_commit_instructions` tool and follow the steps.
   - Run `make all`.

3. **Submit**
   - Use the submit tool.
