import string
from hypothesis import given, strategies as st
from taipanstack.security.validators import validate_url, validate_email

@given(st.text())
def test_fuzz_validate_url(url):
    try:
        validate_url(url)
    except (ValueError, TypeError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script.py"])
