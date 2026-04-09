import coverage
cov = coverage.Coverage(source=['taipanstack.security.sanitizers'], branch=True)
cov.start()

from taipanstack.security.sanitizers import sanitize_env_value

# Case 1: "\x00" in value, len(result) <= max_length
sanitize_env_value("a\x00b", max_length=5, allow_multiline=True)

# Case 2: v_len > max_length, "\x00" in value, len(result) <= max_length
sanitize_env_value("a\x00\x00\x00\x00b", max_length=5, allow_multiline=True)

cov.stop()
cov.save()
cov.report(show_missing=True)
