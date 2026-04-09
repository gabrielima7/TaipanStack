from taipanstack.security.sanitizers import sanitize_env_value

# we need: len(result) > max_length to be FALSE.
# so len(result) <= max_length
# and we need to pass `if v_len <= max_length and "\x00" not in value:`
# so either v_len > max_length OR "\x00" in value.

res1 = sanitize_env_value("a\x00b", max_length=5, allow_multiline=True)
print(f"res1: {repr(res1)}")
