import contextlib

import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.validators import _check_project_name_chars


@given(st.text())
def test_fuzz_project_name_chars(text):
    if text == "":
        try:
            _check_project_name_chars(text, True, True)
        except ValueError:
            pass
        except IndexError:
            pytest.fail("IndexError was raised instead of ValueError")
    else:
        with contextlib.suppress(ValueError):
            _check_project_name_chars(text, True, True)
