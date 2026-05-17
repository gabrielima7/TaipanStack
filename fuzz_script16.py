import string
import re
from hypothesis import given, strategies as st
from taipanstack.security.validators import _check_project_name_chars

@given(st.text())
def test_fuzz_project_name_chars_regex(text):
    if not text:
        return
    try:
        _check_project_name_chars(text, True, True)
    except Exception as e:
        if isinstance(e, IndexError):
            print(f"Exception for text {text}: {type(e)}")
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "-s", "fuzz_script16.py"])
