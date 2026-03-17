import pytest
from hypothesis import given, settings, strategies as st
from taipanstack.security.sanitizers import sanitize_env_value, sanitize_sql_identifier

@given(st.one_of(st.integers(), st.floats(), st.none(), st.lists(st.text()), st.dictionaries(st.text(), st.text())))
@settings(max_examples=100)
def test_fuzz_sanitize_env_value_invalid_types(value):
    with pytest.raises(TypeError, match="value must be str, got"):
        sanitize_env_value(value)

@given(st.one_of(st.integers(), st.floats(), st.none(), st.lists(st.text()), st.dictionaries(st.text(), st.text())))
@settings(max_examples=100)
def test_fuzz_sanitize_sql_identifier_invalid_types(value):
    with pytest.raises(TypeError, match="identifier must be str, got"):
        sanitize_sql_identifier(value)
