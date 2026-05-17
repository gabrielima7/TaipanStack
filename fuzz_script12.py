import string
import re
from hypothesis import given, strategies as st
from taipanstack.security.validators import _check_project_name_chars

@given(st.text())
def test_fuzz_project_name_chars_regex(text):
    if not text or not text[0].isalpha():
        return
    try:
        _check_project_name_chars(text, True, True)
    except (ValueError, TypeError, IndexError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script12.py"])
