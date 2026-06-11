from urllib.parse import unquote

from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_url

control_char_url_encoded_strategy = st.builds(
    lambda c: f"https://example.com/%{ord(c):02x}foo", st.characters(max_codepoint=0x20)
)


@given(url=control_char_url_encoded_strategy)
@settings(max_examples=100)
def test_url_smuggling_bypass_expected(url: str) -> None:
    try:
        validated = validate_url(url)
        unquoted = unquote(validated)
        assert not any(c <= "\x20" or c == "\x7f" for c in unquoted)
    except ValueError:
        pass
