from hypothesis import given, settings
from hypothesis import strategies as st
from src.taipanstack.security.sanitizers import sanitize_filename, sanitize_string
from src.taipanstack.security.validators import _fully_unquote_url


@settings(max_examples=100)
@given(st.text())
def test_security_validators_fully_unquote_url_fuzz(url):
    try:
        res = _fully_unquote_url(url)
        assert isinstance(res, str)
    except ValueError as e:
        assert (
            "exceeds maximum nested encoding limit" in str(e)
            or "invalid" in str(e).lower()
        )


@settings(max_examples=100)
@given(st.text())
def test_security_sanitizers_sanitize_string_fuzz(s):
    try:
        res = sanitize_string(s, max_length=100)
        assert len(res) <= 100
    except ValueError as e:
        assert "exceeds maximum allowed limit" in str(e)


@settings(max_examples=100)
@given(st.text())
def test_security_sanitizers_sanitize_filename_fuzz(f):
    try:
        res = sanitize_filename(f, max_length=100)
        assert len(res) <= 100
        assert "/" not in res
        assert "\\" not in res
    except ValueError as e:
        assert "exceeds maximum allowed limit" in str(e)
