import timeit
import taipanstack.core.result as result

setup = """
from taipanstack.core.result import Result, Ok, Err, collect_results, _collect_list
oks = [Ok(i) for i in range(100)]
"""

new_time = timeit.timeit('_collect_list(oks)', setup=setup, number=100000)
print(f'New collect list: {new_time:.4f}')

setup_old = """
from taipanstack.core.result import Result, Ok, Err, collect_results
oks = [Ok(i) for i in range(100)]
def _collect_list(results):
    try:
        return Ok([r.ok_value for r in results])
    except AttributeError:
        return None
"""
old_time = timeit.timeit('_collect_list(oks)', setup=setup_old, number=100000)
print(f'Old collect list: {old_time:.4f}')
