from taipanstack.core.result import Ok, Err, collect_results
import timeit

res_list = [Ok(i) for i in range(100)]
def collect_results_opt2(results):
    try:
        if type(results) in (list, tuple):
            return Ok([r.ok_value for r in results])
        else:
            return Ok([r.ok_value for r in results])
    except AttributeError:
        # One of them is Err, we must find it
        for r in results:
            if not isinstance(r, Ok):
                return r

print(timeit.timeit(lambda: collect_results(res_list), number=10000))
print(timeit.timeit(lambda: collect_results_opt2(res_list), number=10000))
