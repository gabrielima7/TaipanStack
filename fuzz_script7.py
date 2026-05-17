import string
from hypothesis import given, strategies as st
from taipanstack.security.validators import validate_project_name

@given(st.text())
def test_fuzz_project_name(text):
    try:
        validate_project_name(text)
    except (ValueError, TypeError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script7.py"])
