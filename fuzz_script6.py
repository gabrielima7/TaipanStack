import string
from hypothesis import given, strategies as st
from taipanstack.security.validators import _check_version_format, _check_email_basics, _check_url_basics

@given(st.text())
def test_fuzz_version_format(text):
    try:
        _check_version_format(text)
    except (ValueError, TypeError):
        pass

@given(st.text())
def test_fuzz_email_basics(text):
    try:
        _check_email_basics(text)
    except (ValueError, TypeError):
        pass

@given(st.text())
def test_fuzz_url_basics(text):
    try:
        _check_url_basics(text)
    except (ValueError, TypeError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script6.py"])
