from taipanstack.security.guards import guard_command_injection

def empty_gen():
    if False: yield 1

print(guard_command_injection(empty_gen()))
