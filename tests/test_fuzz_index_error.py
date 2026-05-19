import contextlib

import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.validators import _check_project_name_chars


@given(st.text())
def test_validators_project_name_chars_fuzz_rejects_empty_without_index_error(text):
    if text == "":
        with pytest.raises(ValueError):
            _check_project_name_chars(text, True, True)
    else:
        with contextlib.suppress(ValueError):
            _check_project_name_chars(text, True, True)
