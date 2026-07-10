import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import SecurityError, guard_path_traversal


@settings(
    max_examples=5,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
)
@given(path=st.text(min_size=4097, max_size=5000))
def test_fuzz_guard_path_traversal_exceeds_max_path_length_expected(path):
    with pytest.raises(SecurityError):
        guard_path_traversal(path)


@settings(
    max_examples=5,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
)
@given(base_dir=st.text(min_size=4097, max_size=5000))
def test_fuzz_guard_path_traversal_base_dir_exceeds_max_path_length_expected(
    base_dir,
):
    with pytest.raises(SecurityError):
        guard_path_traversal("a", base_dir=base_dir)
