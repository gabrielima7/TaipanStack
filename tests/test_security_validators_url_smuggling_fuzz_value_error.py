from urllib.parse import quote

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_url


@settings(max_examples=100)
@given(st.text(alphabet=st.characters(categories=["Cc"]), min_size=1, max_size=10))
def test_security_validators_url_smuggling_fuzz_value_error(control_char: str) -> None:
    # Double-encode control char.
    # url will have %25XX.
    # validate_url will do unquote once -> %XX, which is printable!
    # But later, when passed to a request library, it might unquote again -> control char! (SSRF/Smuggling)
    # The fix is to recursively unquote until it stops changing, then check.

    double_encoded = quote(quote(control_char))
    url = f"https://example.com/path?q={double_encoded}"

    # We want this to raise ValueError as it ultimately contains a control char.
    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url)
