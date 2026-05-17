import string
from hypothesis import given, strategies as st
from taipanstack.security.validators import _check_project_name_chars

@given(st.text(), st.booleans(), st.booleans())
def test_fuzz_project_name_chars(text, allow_h, allow_u):
    try:
        _check_project_name_chars(text, allow_h, allow_u)
    except (ValueError, TypeError, IndexError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script10.py"])
