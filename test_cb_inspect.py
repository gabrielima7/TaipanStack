from taipanstack.resilience.circuit_breaker import circuit_breaker
@circuit_breaker(failure_threshold=1, timeout=1.0)
def my_func():
    pass
print(my_func.__closure__)
for cell in my_func.__closure__:
    print(cell.cell_contents)
