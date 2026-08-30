import pytest
from hypothesis import given
from hypothesis import strategies as st

from taipanstack.security.validators import _check_project_name_chars


@given(st.text())
def test_fuzz_index_error_validators_project_name_chars_fuzz_rejects_empty_without_index_error(
    text,
):
    if text == "":
        with pytest.raises(ValueError):
            _check_project_name_chars(text, True, True)
    else:
        # Fuzzing produces both valid and invalid text.
        # When invalid, it should only raise ValueError.
        try:
            _check_project_name_chars(text, True, True)
        except ValueError as e:
            assert isinstance(e, ValueError)
