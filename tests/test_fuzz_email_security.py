"""Property-based fuzz testing for validate_email."""

import contextlib

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_email


@given(st.text(min_size=2048, max_size=4096))
@settings(
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    max_examples=10,
)
def test_fuzz_validate_email_massive_strings(email_str: str) -> None:
    """Fuzz validate_email with massive strings to check for DoS/ReDoS."""
    with pytest.raises(ValueError):
        validate_email(email_str)


@given(
    st.text(
        alphabet=st.characters(
            categories=("Lu", "Ll", "Nd", "Zs"), include_characters="._%+-\n\x00"
        ),
        min_size=1,
        max_size=100,
    )
)
@settings(max_examples=100)
def test_fuzz_validate_email_edge_cases(email_str: str) -> None:
    """Fuzz validate_email with unprintable chars and near-valid inputs."""
    with contextlib.suppress(ValueError):
        validate_email(email_str)
