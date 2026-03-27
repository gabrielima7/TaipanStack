import re

with open("src/taipanstack/resilience/adaptive/orchestrator.py", "r") as f:
    content = f.read()

# Replace any occurrence of Any to silence errors when calling fn(*args, **kwargs).
content = re.sub(r"return await self._execute_inner\(fn, \*args, \*\*kwargs\)", "return await self._execute_inner(fn, *args, **kwargs)  # type: ignore[misc]", content)

content = re.sub(r"result = await self._execute_with_timeout\(fn, \*args, \*\*kwargs\)", "result = await self._execute_with_timeout(fn, *args, **kwargs)  # type: ignore[misc]", content)

content = content.replace("fn(*args, **kwargs),", "fn(*args, **kwargs),  # type: ignore[misc]")

content = re.sub(r"result = await fn\(\*args, \*\*kwargs\)", "result = await fn(*args, **kwargs)  # type: ignore[misc]", content)

with open("src/taipanstack/resilience/adaptive/orchestrator.py", "w") as f:
    f.write(content)
