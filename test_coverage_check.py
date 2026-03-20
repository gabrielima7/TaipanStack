"""Test module for URL validation coverage."""
from taipanstack.security.validators import validate_url

try:
    validate_url("http://example.", require_tld=True)
except ValueError as e:
    print(f"Error: {e}")  # noqa: T201

try:
    validate_url("http://example:", require_tld=True)
except ValueError as e:
    print(f"Error: {e}")  # noqa: T201

try:
    validate_url("http://example:80", require_tld=True)
except ValueError as e:
    print(f"Error: {e}")  # noqa: T201
