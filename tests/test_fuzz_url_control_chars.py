from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Err
from taipanstack.security.guards import guard_ssrf
from taipanstack.security.validators import validate_url


@settings(max_examples=100)
@given(st.text())
def test_fuzz_url_control_chars_validators(text: str) -> None:
    has_control = any(c <= "\x20" or c == "\x7f" for c in text)
    try:
        validate_url(text)
    except ValueError:
        pass
    else:
        if has_control:
            msg = f"Bypass found for URL with control chars: {text!r}"
            raise AssertionError(msg)



@settings(max_examples=100)
@given(st.text())
def test_fuzz_url_control_chars_guards(text: str) -> None:
    has_control = any(c <= "\x20" or c == "\x7f" for c in text)
    res = guard_ssrf(text)
    if isinstance(res, Err):
        assert "SecurityError" in str(type(res.err_value))
    elif has_control:
        # If it returned Ok but has control chars, that's a bypass!
        msg = f"Bypass found for URL with control chars: {text!r}"
        raise AssertionError(msg)
