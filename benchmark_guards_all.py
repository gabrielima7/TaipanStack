import timeit

setup = """
from taipanstack.security.guards import guard_command_injection, guard_path_traversal, guard_file_extension, guard_env_variable
import os
os.environ['MY_VAR'] = 'test_value'
"""

cmd_inj = "guard_command_injection(['echo', 'hello', 'world'])"
path_trav = "guard_path_traversal('a/b/c.txt')"
file_ext = "guard_file_extension('image.png')"
env_var = "guard_env_variable('MY_VAR')"

print("cmd_inj:", timeit.timeit(cmd_inj, setup=setup, number=100000))
print("path_trav:", timeit.timeit(path_trav, setup=setup, number=10000))
print("file_ext:", timeit.timeit(file_ext, setup=setup, number=100000))
print("env_var:", timeit.timeit(env_var, setup=setup, number=100000))
