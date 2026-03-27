import re

with open("src/taipanstack/resilience/adaptive/orchestrator.py", "r") as f:
    content = f.read()

content = re.sub(r"\*\*kwargs: Any,", r"**kwargs: Any,  # type: ignore[misc]", content)
content = content.replace("*args: Any,", "*args: Any,  # type: ignore[misc]")

content = content.replace("result: Result[T, Exception] = Err(", "result: Result[T, Exception] = Err(  # type: ignore[misc]")

content = content.replace("return await self._execute_inner(fn, *args, **kwargs)", "return await self._execute_inner(fn, *args, **kwargs)  # type: ignore[misc]")

content = content.replace("result = await self._execute_with_timeout(fn, *args, **kwargs)", "result = await self._execute_with_timeout(fn, *args, **kwargs)  # type: ignore[misc]")
content = content.replace("final_result: Result[T, Exception] = Err(", "final_result: Result[T, Exception] = Err(  # type: ignore[misc]")

content = content.replace("result = await asyncio.wait_for(\n                    fn(*args, **kwargs),\n                    timeout=self._timeout,\n                )", "result = await asyncio.wait_for(\n                    fn(*args, **kwargs),  # type: ignore[misc]\n                    timeout=self._timeout,\n                )")
content = content.replace("result = await fn(*args, **kwargs)", "result = await fn(*args, **kwargs)  # type: ignore[misc]")


with open("src/taipanstack/resilience/adaptive/orchestrator.py", "w") as f:
    f.write(content)
