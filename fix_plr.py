with open("src/taipanstack/resilience/circuit_breaker.py", "r") as f:
    content = f.read()

import re

search = """                case CircuitState.CLOSED:
                    pass"""

replace = """                case CircuitState.CLOSED:
                    return True"""

new_content = content.replace(search, replace)

search_return = """        return False  # pragma: no cover — unreachable, satisfies type checker"""

replace_return = """        return True"""

new_content = new_content.replace(search_return, replace_return)

with open("src/taipanstack/resilience/circuit_breaker.py", "w") as f:
    f.write(new_content)
