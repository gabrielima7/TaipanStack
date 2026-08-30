import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import (
    validate_email,
    validate_project_name,
    validate_url,
)


def test_fuzz_extreme_limits_dos_fuzz_project_name_massive_dos() -> None:
    """Fuzz validate_project_name with massive strings."""
    name = "a" * (10**5)
    with pytest.raises(ValueError):
        validate_project_name(name, max_length=100)  # Force length fail


def test_fuzz_extreme_limits_dos_fuzz_url_massive_dos() -> None:
    """Fuzz validate_url with massive strings."""
    url = "a" * (10**5)
    with pytest.raises(ValueError):
        validate_url(url)


def test_fuzz_extreme_limits_dos_fuzz_email_massive_dos() -> None:
    """Fuzz validate_email with massive strings."""
    email = "a" * (10**5)
    with pytest.raises(ValueError):
        validate_email(email)


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=5,
)
@given(name=st.text(min_size=10**3, max_size=10**3 + 10))
def test_fuzz_extreme_limits_dos_fuzz_project_name_hypothesis_dos(name: str) -> None:
    """Fuzz validate_project_name with massive strings."""
    with pytest.raises(ValueError):
        validate_project_name(name, max_length=100)  # Force length fail


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=5,
)
@given(url=st.text(min_size=10**3, max_size=10**3 + 10))
def test_fuzz_extreme_limits_dos_fuzz_url_hypothesis_dos(url: str) -> None:
    """Fuzz validate_url with massive strings."""
    with pytest.raises(ValueError):
        validate_url(url)


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=5,
)
@given(email=st.text(min_size=10**3, max_size=10**3 + 10))
def test_fuzz_extreme_limits_dos_fuzz_email_hypothesis_dos(email: str) -> None:
    """Fuzz validate_email with massive strings."""
    with pytest.raises(ValueError):
        validate_email(email)
