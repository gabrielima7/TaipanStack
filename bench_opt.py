import re
import timeit

identifier = "user_accounts_table"
pattern_str = r"[^a-zA-Z0-9_]"
pattern_re = re.compile(pattern_str)

def original():
    return re.sub(pattern_str, "", identifier)

def precompiled():
    return pattern_re.sub("", identifier)

def fast_path():
    if pattern_re.search(identifier):
        return pattern_re.sub("", identifier)
    return identifier

print(f"Original: {timeit.timeit(original, number=1000000)}")
print(f"Precompiled: {timeit.timeit(precompiled, number=1000000)}")
print(f"Fast path: {timeit.timeit(fast_path, number=1000000)}")
