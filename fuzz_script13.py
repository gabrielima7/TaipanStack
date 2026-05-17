import string
import re
from hypothesis import given, strategies as st
from taipanstack.security.validators import _check_project_name_reserved

@given(st.text())
def test_fuzz_project_name_reserved(text):
    try:
        _check_project_name_reserved(text)
    except (ValueError, TypeError, IndexError):
        pass

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "fuzz_script13.py"])
