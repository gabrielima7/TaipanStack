from result import Ok, Err
import time

def collect_results_old(results):
    if type(results) in (list, tuple):
        try:
            return Ok([r.ok_value for r in results])
        except AttributeError:
            pass

    values = []
    append = values.append
    for result in results:
        if isinstance(result, Ok):
            append(result.ok_value)
        elif isinstance(result, Err):
            return result
        else:
            return result
    return Ok(values)

def collect_results_new(results):
    if type(results) in (list, tuple):
        try:
            return Ok([r._value for r in results])
        except AttributeError:
            pass

    values = []
    append = values.append
    for result in results:
        if type(result) is Ok:
            append(result._value)
        elif type(result) is Err:
            return result
        else:
            return result
    return Ok(values)

results = [Ok(i) for i in range(100)]
start = time.time()
for _ in range(100000):
    collect_results_old(results)
print("collect_results_old:", time.time() - start)

start = time.time()
for _ in range(100000):
    collect_results_new(results)
print("collect_results_new:", time.time() - start)
