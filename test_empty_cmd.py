from taipanstack.security.guards import guard_command_injection

def empty_gen():
    yield from ()

try:
    res = guard_command_injection(empty_gen())
    print("Bypassed! Returned:", res)
except Exception as e:
    print("Blocked:", type(e))
