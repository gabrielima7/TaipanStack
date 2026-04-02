import re

with open("src/taipanstack/resilience/resilience.py", "r") as f:
    content = f.read()

content = content.replace("from typing import Any, ParamSpec, Protocol, TypeAlias, TypeVar, cast, overload", "from collections.abc import Awaitable, Callable\nfrom typing import Any, ParamSpec, Protocol, TypeAlias, TypeVar, cast, overload")
content = content.replace("from collections.abc import Callable, Coroutine", "")
content = content.replace("Callable[P, Coroutine[Any, Any, Result[T, E]]]", "Callable[P, Awaitable[Result[T, E]]]")
content = content.replace("Callable[P, Coroutine[Any, Any, Result[T, TimeoutError | E]]]", "Callable[P, Awaitable[Result[T, TimeoutError | E]]]")
content = content.replace("Coroutine", "Awaitable")

with open("src/taipanstack/resilience/resilience.py", "w") as f:
    f.write(content)
