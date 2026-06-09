from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import MAX_PATH_LENGTH, sanitize_string


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    max_examples=5,
    deadline=None,
)
@given(st.text(min_size=MAX_PATH_LENGTH + 1, max_size=MAX_PATH_LENGTH + 50))
def test_fuzz_sanitize_string_dos_hypothesis_standard_expected(value: str) -> None:
    import pytest
    with pytest.raises(ValueError, match="String length exceeds maximum allowed"):
        sanitize_string(value)
