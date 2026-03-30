from taipanstack.core.result import Ok, Err, collect_results
import timeit

res_list = [Ok(i) for i in range(100)]
res_iter = lambda: (Ok(i) for i in range(100))

def collect_results_opt4(results):
    if type(results) in (list, tuple):
        values = []
        append = values.append
        for r in results:
            try:
                append(r.ok_value)
            except AttributeError:
                return r
        return Ok(values)
    else:
        values = []
        append = values.append
        for r in results:
            try:
                append(r.ok_value)
            except AttributeError:
                return r
        return Ok(values)

print("list")
print(timeit.timeit(lambda: collect_results_opt4(res_list), number=10000))
print("iter")
print(timeit.timeit(lambda: collect_results_opt4(res_iter()), number=10000))
