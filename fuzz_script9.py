import string
from hypothesis import given, strategies as st
from taipanstack.security.validators import validate_project_name

@given(st.text(), st.integers())
def test_fuzz_project_name_length(text, length):
    try:
        validate_project_name(text, max_length=length)
    except (ValueError, TypeError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script9.py"])
