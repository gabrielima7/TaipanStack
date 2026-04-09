import coverage
cov = coverage.Coverage(source=['taipanstack.security.sanitizers'])
cov.start()

from taipanstack.security.sanitizers import sanitize_env_value

# Try hitting 427 with multiline=False?
# No, multiline=False logic is lines 408-419
# Wait! Let's check `if not allow_multiline:` block (lines 408-419):

#         if (
#             v_len <= max_length
#             and "\n" not in value
#             and "\r" not in value
#             and "\x00" not in value
#         ):
#             return value
#         result = value.replace("\x00", "").replace("\n", " ").replace("\r", " ")
#         if len(result) > max_length:
#             return result[:max_length]
#         return result  # <-- THIS MIGHT BE LINE 419. WAIT, where is 427?

# Let's just run EVERYTHING we can think of
print(repr(sanitize_env_value("a\nb", max_length=5, allow_multiline=True)))
print(repr(sanitize_env_value("a\x00b", max_length=5, allow_multiline=True)))
print(repr(sanitize_env_value("a\n" * 10, max_length=5, allow_multiline=True)))
print(repr(sanitize_env_value("a\x00b" * 10, max_length=5, allow_multiline=True)))

print(repr(sanitize_env_value("a\nb", max_length=5, allow_multiline=False)))
print(repr(sanitize_env_value("a\x00b", max_length=5, allow_multiline=False)))
print(repr(sanitize_env_value("a\n" * 10, max_length=5, allow_multiline=False)))
print(repr(sanitize_env_value("a\x00b" * 10, max_length=5, allow_multiline=False)))

# What if v_len > max_length, but \x00 NOT in value, and len(result) <= max_length?
# Only possible if value length is > max_length but we somehow shrink it?
# In multiline=True: we only replace \x00. So we can't shrink it without \x00.
# So if \x00 is NOT in value, `len(result)` == `v_len`.
# So if v_len > max_length, then len(result) > max_length is TRUE.
# Meaning 427 CANNOT be reached if "\x00" not in value AND v_len > max_length.

# BUT wait! Does mypy or coverage consider the implicit `else` branch of `if len(result) > max_length:`?
# If `len(result) <= max_length` we hit `return result`.
# If `len(result) > max_length` we hit `return result[:max_length]`.
# Is it possible that `len(result) == max_length` is not hit?
print(repr(sanitize_env_value("a\x00b", max_length=2, allow_multiline=True)))

cov.stop()
cov.save()
cov.report(show_missing=True)
