import re

with open("src/taipanstack/resilience/retry.py", "r") as f:
    content = f.read()

content = content.replace("from typing import Any, NoReturn, ParamSpec, Protocol, TypeVar, cast, overload", "from typing import Any, Callable, Coroutine, NoReturn, ParamSpec, Protocol, TypeVar, cast, overload")

with open("src/taipanstack/resilience/retry.py", "w") as f:
    f.write(content)
