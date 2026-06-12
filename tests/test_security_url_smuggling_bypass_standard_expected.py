from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_url

control_char_url_encoded_strategy = st.builds(
    lambda c: f"https://example.com/%{ord(c):02x}foo", st.characters(max_codepoint=0x20)
)


@given(url=control_char_url_encoded_strategy)
@settings(max_examples=100)
def test_security_url_smuggling_bypass_standard_expected(url: str) -> None:
    import pytest

    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url)
