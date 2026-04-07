from result import Ok
from taipanstack.core.result import collect_results
import time
import pytest_benchmark

results = [Ok(i) for i in range(100)]
start = time.time()
for _ in range(100000):
    collect_results(results)
print("collect_results:", time.time() - start)
