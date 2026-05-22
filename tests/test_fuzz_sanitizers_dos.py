import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import (
    MAX_ENV_VALUE_LENGTH,
    MAX_PATH_LENGTH,
    sanitize_env_value,
    sanitize_filename,
    sanitize_sql_identifier,
)


# Testing Massive Lengths (DoS) using simple parameters because Hypothesis
# has maximum string length limits around 65535 chars which aren't large enough.
def test_fuzz_sanitizers_dos_sanitize_filename_massive() -> None:
    filename = "a" * (MAX_PATH_LENGTH + 1)
    with pytest.raises(
        ValueError, match="Filename length exceeds maximum allowed limit"
    ):
        sanitize_filename(filename)


def test_fuzz_sanitizers_dos_sanitize_sql_identifier_massive() -> None:
    identifier = "a" * (MAX_PATH_LENGTH + 1)
    with pytest.raises(
        ValueError, match="SQL identifier length exceeds maximum allowed limit"
    ):
        sanitize_sql_identifier(identifier)


def test_fuzz_sanitizers_dos_sanitize_env_value_massive() -> None:
    value = "a" * (MAX_ENV_VALUE_LENGTH + 1)
    with pytest.raises(
        ValueError, match="Environment value length exceeds maximum allowed limit"
    ):
        sanitize_env_value(value)


# Also test null bytes, as requested by instructions
@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cc",), whitelist_characters=["\x00"]
        ),
        min_size=1,
        max_size=100,
    ).filter(lambda s: "\x00" in s)
)
def test_fuzz_sanitizers_dos_sanitize_env_value_null_bytes(value: str) -> None:
    # Ensure it doesn't crash on null bytes, it sanitizes them away
    result = sanitize_env_value(value)
    assert "\x00" not in result
