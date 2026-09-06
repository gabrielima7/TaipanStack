import contextlib
from urllib.parse import quote

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.validators import validate_email, validate_url


@settings(
    max_examples=10,
    deadline=None,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.filter_too_much,
        HealthCheck.data_too_large,
    ],
)
@given(st.text(min_size=2000, max_size=3000))
def test_fuzz_url_dos(text: str) -> None:
    with contextlib.suppress(ValueError):
        url = "https://example.com/" + quote(text)
        validate_url(url)


@settings(
    max_examples=10,
    deadline=None,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.filter_too_much,
        HealthCheck.data_too_large,
    ],
)
@given(st.text(min_size=2000, max_size=3000))
def test_fuzz_email_dos(text: str) -> None:
    with contextlib.suppress(ValueError):
        validate_email(text)
