from taipanstack.core.result import Ok, Err, collect_results
import timeit

res_list = [Ok(i) for i in range(100)]
res_iter = lambda: (Ok(i) for i in range(100))

def collect_results_opt3(results):
    if type(results) in (list, tuple):
        try:
            return Ok([r.ok_value for r in results])
        except AttributeError:
            for r in results:
                try:
                    r.ok_value
                except AttributeError:
                    return r
    else:
        values = []
        append = values.append
        for result in results:
            try:
                append(result.ok_value)
            except AttributeError:
                return result
        return Ok(values)

print("list")
print(timeit.timeit(lambda: collect_results(res_list), number=10000))
print(timeit.timeit(lambda: collect_results_opt3(res_list), number=10000))
print("iter")
print(timeit.timeit(lambda: collect_results(res_iter()), number=10000))
print(timeit.timeit(lambda: collect_results_opt3(res_iter()), number=10000))
