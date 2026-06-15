with open("src/taipanstack/resilience/retry.py", "r", encoding="utf-8") as f:
    content = f.read()

# I see what's happening. My helper returns False, 0.0 when it should break.
# But it *already* logged the "all failed" message.
# Wait, why are those tests failing?
# Let's inspect one of the test failures in detail:
import pytest
