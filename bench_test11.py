from result import Ok, Err
import time

def collect_results_1(results):
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

def collect_results_2(results):
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
    collect_results_1(results)
print("collect_results_1:", time.time() - start)

start = time.time()
for _ in range(100000):
    collect_results_2(results)
print("collect_results_2:", time.time() - start)

results_tuple = tuple(Ok(i) for i in range(100))
start = time.time()
for _ in range(100000):
    collect_results_1(results_tuple)
print("collect_results_1 (tuple):", time.time() - start)

start = time.time()
for _ in range(100000):
    collect_results_2(results_tuple)
print("collect_results_2 (tuple):", time.time() - start)
