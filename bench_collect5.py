from taipanstack.core.result import Ok, Err, collect_results
import timeit

res_list = [Ok(i) for i in range(100)]

def collect_results_opt5(results):
    if type(results) in (list, tuple):
        try:
            return Ok([r.ok_value for r in results])
        except AttributeError:
            pass

    values = []
    append = values.append
    for result in results:
        try:
            append(result.ok_value)
        except AttributeError:
            return result
    return Ok(values)

print(timeit.timeit(lambda: collect_results_opt5(res_list), number=10000))
