from result import Ok, Err
import inspect

r = Err(ValueError("err"))
print(dir(r))
print(hasattr(r, "_value"))
print(r._value)
