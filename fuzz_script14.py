import string
import re
from hypothesis import given, strategies as st
from taipanstack.security.validators import _check_version_numbers

@given(st.text())
def test_fuzz_version_numbers(text):
    try:
        _check_version_numbers(text)
    except (ValueError, TypeError, IndexError, Exception):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script14.py"])
