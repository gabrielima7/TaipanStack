import timeit

setup = """
from taipanstack.security.guards import guard_command_injection
"""

command = "guard_command_injection(['echo', 'hello'])"

print(timeit.timeit(command, setup=setup, number=100000))
