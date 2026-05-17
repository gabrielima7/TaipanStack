import string
import re
from hypothesis import given, strategies as st
from taipanstack.security.validators import _check_project_name_chars

@given(st.text())
def test_fuzz_empty(text):
    if text == "":
        try:
            _check_project_name_chars(text, True, True)
        except Exception as e:
            print(f"Exception for empty string: {type(e)}")

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "-s", "fuzz_script15.py"])
