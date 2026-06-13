import sys
import re

filepath = "src/taipanstack/resilience/adaptive/orchestrator.py"
with open(filepath, "r") as f:
    content = f.read()

# Make it timeout-safe by using asyncio.wait_for properly or returning Err instead of throwing?
# But timeout is not currently implemented in the orchestrator execution. Let's see orchestrator.py
