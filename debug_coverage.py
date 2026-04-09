from taipanstack.security.sanitizers import sanitize_env_value

import coverage
cov = coverage.Coverage(source=['taipanstack.security.sanitizers'])
cov.start()

# Let's hit EVERY branch in the multiline block
# Block:
#     if v_len <= max_length and "\x00" not in value:
#         return value
#
#     result = value.replace("\x00", "")
#     if len(result) > max_length:
#         return result[:max_length]
#     return result

print(repr(sanitize_env_value("a\nb", max_length=5, allow_multiline=True))) # Hits `return value`
print(repr(sanitize_env_value("a\x00b", max_length=5, allow_multiline=True))) # `v_len <= max_length` but `\x00` in value. `len(result) <= max_length`, returns at 427.
print(repr(sanitize_env_value("a\n" * 10, max_length=5, allow_multiline=True))) # `v_len > max_length`, `\x00` not in value. `len(result) > max_length`, returns at 426.
print(repr(sanitize_env_value("a\x00b" * 10, max_length=5, allow_multiline=True))) # `v_len > max_length`, `\x00` in value. `len(result) > max_length`, returns at 426.

cov.stop()
cov.save()
cov.report(show_missing=True)
