from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

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
def test_fuzz_guard_ssrf_malformed(s: str) -> None:
    """Fuzz guard_ssrf with extreme and malformed string inputs."""
    # Since we are fuzzing with pure random text, most strings will fail URL validation
    # However, our goal is to ensure it returns an Err() or Ok() and doesn't throw unhandled exceptions
    guard_ssrf(s)
