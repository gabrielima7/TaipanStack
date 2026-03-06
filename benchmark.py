import time
import timeit
from taipanstack.security.guards import guard_path_traversal

def run_benchmark():
    # Warmup
    for _ in range(100):
        guard_path_traversal("safe/path/to/file.txt")

    # Bench
    setup = """
from taipanstack.security.guards import guard_path_traversal
"""
    stmt = """
guard_path_traversal("some/very/long/and/safe/path/to/some/nested/file/that/is/fine.txt")
"""
    times = timeit.repeat(stmt, setup=setup, number=10000, repeat=5)
    print(f"Baseline (safe): {min(times):.4f}s")

    stmt2 = """
try:
    guard_path_traversal("some/very/long/and/safe/path/to/some/nested/file/that/is/../fine.txt")
except Exception:
    pass
"""
    times2 = timeit.repeat(stmt2, setup=setup, number=10000, repeat=5)
    print(f"Baseline (unsafe): {min(times2):.4f}s")

if __name__ == "__main__":
    run_benchmark()
