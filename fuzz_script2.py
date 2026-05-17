import string
from hypothesis import given, strategies as st
from taipanstack.security.validators import validate_python_version, validate_email, validate_url

@given(st.text())
def test_fuzz_validate_python_version(version):
    try:
        validate_python_version(version)
    except (ValueError, TypeError):
        pass

@given(st.text())
def test_fuzz_validate_email(email):
    try:
        validate_email(email)
    except (ValueError, TypeError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script2.py"])
