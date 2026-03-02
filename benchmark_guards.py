import timeit

setup_code = """
import os
from src.taipanstack.security.guards import (
    guard_file_extension,
    guard_env_variable,
    guard_command_injection,
    guard_path_traversal
)
os.environ["SAFE_VAR"] = "1"
"""

benchmark_file_ext = """
try:
    guard_file_extension("test.txt", allowed_extensions=["txt"])
except Exception:
    pass
"""

benchmark_env_var = """
try:
    guard_env_variable("SAFE_VAR", allowed_names=["SAFE_VAR"])
except Exception:
    pass
"""

benchmark_cmd = """
try:
    guard_command_injection(["ls", "-l"])
except Exception:
    pass
"""

benchmark_path = """
try:
    guard_path_traversal("test.txt")
except Exception:
    pass
"""


if __name__ == "__main__":
    n = 100000
    t_file = timeit.timeit(benchmark_file_ext, setup=setup_code, number=n)
    t_env = timeit.timeit(benchmark_env_var, setup=setup_code, number=n)
    t_cmd = timeit.timeit(benchmark_cmd, setup=setup_code, number=n)
    t_path = timeit.timeit(benchmark_path, setup=setup_code, number=n)

    print(f"guard_file_extension: {t_file:.5f}s for {n} runs")
    print(f"guard_env_variable: {t_env:.5f}s for {n} runs")
    print(f"guard_command_injection: {t_cmd:.5f}s for {n} runs")
    print(f"guard_path_traversal: {t_path:.5f}s for {n} runs")
