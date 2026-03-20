from taipanstack.security.validators import validate_url

try:
    validate_url("http://example.", require_tld=True)
except ValueError as e:
    print(f"Error for http://example.: {e}")

try:
    validate_url("http://example:", require_tld=True)
except ValueError as e:
    print(f"Error for http://example:: {e}")

try:
    validate_url("http://example:80", require_tld=True)
except ValueError as e:
    print(f"Error for http://example:80: {e}")
