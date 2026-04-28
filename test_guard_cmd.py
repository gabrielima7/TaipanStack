from taipanstack.security.guards import guard_command_injection

def my_gen():
    if False: yield 1

print(guard_command_injection(my_gen()))
