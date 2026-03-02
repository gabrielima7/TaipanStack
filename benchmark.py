import timeit

setup_code = """
from taipanstack.security.guards import guard_path_traversal
from pathlib import Path
base = Path('/tmp')
"""

test_code = """
guard_path_traversal("safe_file.txt", base)
"""

iterations = 100000
time_taken = timeit.timeit(stmt=test_code, setup=setup_code, number=iterations)
print(f"Time for {iterations} iterations: {time_taken:.4f} seconds")
