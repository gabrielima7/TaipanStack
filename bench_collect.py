from taipanstack.core.result import collect_results, Ok, Err
import timeit

res_list = [Ok(i) for i in range(100)]
def collect_results_opt(results):
    if type(results) in (list, tuple):
        # fast path for list comprehensions
        values = []
        append = values.append
        for result in results:
            try:
                append(result.ok_value)
            except AttributeError:
                return result
        return Ok(values)
    else:
        return collect_results(results)

print(timeit.timeit(lambda: collect_results(res_list), number=10000))
print(timeit.timeit(lambda: collect_results_opt(res_list), number=10000))
