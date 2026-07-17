import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_email


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(st.sampled_from(["\x00", "\x01", "\x08", "\x1f", "\x7f", "\x20"]))
def test_fuzz_email_edge_cases_fuzz_email_control_characters(chars: str) -> None:
    """Fuzz validate_email with control characters."""
    email = f"user@{chars}.com"
    with pytest.raises(
        ValueError, match="Email contains invalid characters|Invalid email format"
    ):
        validate_email(email)
