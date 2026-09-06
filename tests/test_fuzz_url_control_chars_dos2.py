import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from urllib.parse import quote

from taipanstack.security.validators import validate_url, validate_email

@settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow, HealthCheck.large_base_example, HealthCheck.filter_too_much, HealthCheck.data_too_large])
@given(st.text(min_size=8000, max_size=8192))
def test_fuzz_url_dos(text: str) -> None:
    try:
        url = "https://example.com/" + quote(text)
        validate_url(url)
    except ValueError:
        pass

@settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow, HealthCheck.large_base_example, HealthCheck.filter_too_much, HealthCheck.data_too_large])
@given(st.text(min_size=8000, max_size=8192))
def test_fuzz_email_dos(text: str) -> None:
    try:
        validate_email(text)
    except ValueError:
        pass
