import re
import os

files_to_fix = [
    "src/taipanstack/core/result.py",
    "src/taipanstack/resilience/circuit_breaker.py",
    "src/taipanstack/resilience/resilience.py",
    "src/taipanstack/resilience/retry.py",
    "src/taipanstack/security/guards.py",
    "src/taipanstack/security/password.py",
    "src/taipanstack/utils/rate_limit.py",
    "src/taipanstack/utils/subprocess.py"
]

for file in files_to_fix:
    if not os.path.exists(file):
        continue
    with open(file, "r") as f:
        data = f.read()
    data = re.sub(r"\s*# type: ignore\[unreachable\]", "", data)
    with open(file, "w") as f:
        f.write(data)
