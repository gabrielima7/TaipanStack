import re

def re_add_unreachables(filepath, line_nums):
    with open(filepath, "r") as f:
        lines = f.readlines()

    for num in line_nums:
        idx = num - 1
        lines[idx] = lines[idx].rstrip() + "  # type: ignore[unreachable]\n"

    with open(filepath, "w") as f:
        f.writelines(lines)

re_add_unreachables("src/taipanstack/utils/rate_limit.py", [79, 85, 100, 103, 115, 150, 175, 196])
re_add_unreachables("src/taipanstack/resilience/circuit_breaker.py", [292, 382])
