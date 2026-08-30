from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.core.result import Err, Ok
from taipanstack.security.guards import guard_ssrf


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    max_examples=10,
    deadline=None,
)
@given(st.text(min_size=2049, max_size=8192))
def test_fuzz_guard_ssrf_massive_strings_dos_returns_err(
    url: str,
) -> None:
    """Fuzz guard_ssrf with massive strings to ensure DoS protection limits are active."""
    url = "https://" + url
    result = guard_ssrf(url)
    assert result.is_err()
    assert "URL length exceeds" in str(result.unwrap_err())


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
