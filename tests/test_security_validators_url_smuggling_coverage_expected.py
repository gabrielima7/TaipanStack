from urllib.parse import quote

import pytest

from taipanstack.security.validators import validate_url


def test_security_validators_url_smuggling_dos() -> None:
    # To hit line 363 (return False after max iterations),
    # we need to provide a string that recursively unquotes but NEVER produces
    # an invalid character, AND takes MORE than 10 iterations to settle.

    encoded = "20"
    for _ in range(12):
        encoded = "%25" + encoded[1:] if len(encoded) > 2 else "%25" + encoded
    url = f"http://example.com/?q={encoded}"

    assert validate_url(url) == url

def test_security_validators_url_smuggling_invalid() -> None:
    # Needs to be invalid after at least 1 unquote
    # %00 -> \x00
    url = "http://example.com/?q=%00"
    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url)

    url2 = "http://example.com/?q=" + quote("%00") # %2500 -> %00 -> \x00
    with pytest.raises(ValueError, match="URL contains invalid characters"):
        validate_url(url2)

def test_security_validators_url_smuggling_same_string() -> None:
    # To hit line 361 (break when unquoted == current_url):
    # A string with no % encodings.
    url = "http://example.com/?q=valid"
    assert validate_url(url) == url
