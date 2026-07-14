import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import sanitize_string


@settings(max_examples=100)
@given(st.text(), st.integers(min_value=-1000, max_value=-1))
def test_fuzz_sanitize_string_negative_max_length_execution_success(s: str, max_len: int) -> None:
    with pytest.raises(ValueError, match="max_length cannot be negative"):
        sanitize_string(s, max_length=max_len)
