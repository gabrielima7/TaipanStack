from taipanstack.core.result import Ok, Err, collect_results
import timeit

res_list_err = [Ok(i) for i in range(50)] + [Err("e")] + [Ok(i) for i in range(49)]

def collect_results_opt6(results):
    if type(results) in (list, tuple):
        # Do not try list comprehension unless we verify all are ok_value
        # This is essentially the same as doing the loop
        pass

    values = []
    append = values.append
    for result in results:
        try:
            append(result.ok_value)
        except AttributeError:
            return result
    return Ok(values)

print(timeit.timeit(lambda: collect_results(res_list_err), number=10000))
print(timeit.timeit(lambda: collect_results_opt6(res_list_err), number=10000))
