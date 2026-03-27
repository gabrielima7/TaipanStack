with open("src/taipanstack/resilience/adaptive/orchestrator.py", "r") as f:
    content = f.read()

content = content.replace("return Ok(self._fallback_value)", "return Ok(cast(T, self._fallback_value))")

with open("src/taipanstack/resilience/adaptive/orchestrator.py", "w") as f:
    f.write(content)
