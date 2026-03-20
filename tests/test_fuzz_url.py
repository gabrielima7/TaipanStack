import pytest
from hypothesis import given, strategies as st
from taipanstack.security.validators import validate_url

@given(st.text())
def test_fuzz_url(url):
    try:
        validate_url(url)
    except (ValueError, TypeError):
        pass
