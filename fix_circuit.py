with open("src/taipanstack/resilience/circuit_breaker.py", "r") as f:
    lines = f.readlines()

new_lines = []
in_match = False
for line in lines:
    if "match self._state.state:" in line:
        in_match = True

    if in_match and "case CircuitState" in line:
        pass # we're in match
