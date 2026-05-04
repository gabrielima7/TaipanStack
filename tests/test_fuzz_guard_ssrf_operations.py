from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok
from taipanstack.security.guards import guard_ssrf


@given(st.text())
@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    deadline=None,
)
def test_fuzz_guard_ssrf_malformed_returns_ok_or_err(s: str) -> None:
    """Fuzz guard_ssrf with extreme and malformed string inputs."""
    result = guard_ssrf(s)
    assert isinstance(result, (Ok, Err))

def test_guard_ssrf_exceeds_length_returns_err() -> None:
    from taipanstack.security.guards import MAX_URL_LENGTH
    long_url = "http://example.com/" + "a" * (MAX_URL_LENGTH + 1)
    result = guard_ssrf(long_url)
    assert result.is_err()
    assert "length exceeds maximum" in str(result.err_value)
