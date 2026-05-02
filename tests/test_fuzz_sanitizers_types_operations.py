from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import (
    sanitize_env_value,
    sanitize_path,
    sanitize_sql_identifier,
)


@given(
    st.one_of(
        st.integers(),
        st.floats(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100)
def test_fuzz_sanitizers_types_fuzz_sanitize_env_value_invalid_types(value):
    with pytest.raises(TypeError, match="value must be str, got"):
        sanitize_env_value(value)


@given(
    st.one_of(
        st.integers(),
        st.floats(),
        st.none(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
@settings(max_examples=100)
def test_fuzz_sanitizers_types_fuzz_sanitize_sql_identifier_invalid_types(
    value,
):
    with pytest.raises(TypeError, match="identifier must be str, got"):
        sanitize_sql_identifier(value)


def test_fuzz_sanitizers_types_fuzz_sanitize_path_massive_strings() -> None:
    """Fuzz sanitize_path with massive strings to ensure DoS protection limits are active."""
    massive_path = "a/" * 5000
    with pytest.raises(ValueError, match="Path length exceeds maximum allowed"):
        sanitize_path(massive_path)


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    max_examples=5,
    deadline=None,
)
@given(
    st.text(
        alphabet=st.characters(blacklist_characters=["/"]),
        min_size=4097,
        max_size=5000,
    )
)
def test_fuzz_sanitizers_types_fuzz_sanitize_path_hypothesis(
    path: str,
) -> None:
    # Use standard fuzzer to confirm property
    with pytest.raises(ValueError, match="Path length exceeds maximum allowed"):
        sanitize_path(path)


def test_fuzz_sanitizers_types_fuzz_sanitize_path_massive_path_object() -> None:
    """Ensure DoS protection limits are active when passing massive Path objects."""
    massive_path_str = "a" * 5000
    massive_path_obj = Path(massive_path_str)
    with pytest.raises(ValueError, match="Path length exceeds maximum allowed"):
        sanitize_path(massive_path_obj)
