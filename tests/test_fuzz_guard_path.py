from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import SecurityError, guard_path_traversal


@settings(
    suppress_health_check=[HealthCheck.large_base_example, HealthCheck.data_too_large],
    max_examples=100,
)
@given(st.text(min_size=1000, max_size=2000))
def test_fuzz_guard_path_traversal_massive_expected(name: str) -> None:
    """Fuzz guard_path_traversal with massive strings."""
    try:
        guard_path_traversal(name, base_dir=Path("/safe_tmp"))
    except Exception as e:
        assert isinstance(e, (ValueError, TypeError, SecurityError))


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cc",), whitelist_characters=["\x00"]
        ),
        min_size=1,
        max_size=100,
    ).filter(lambda s: "\x00" in s)
)
def test_fuzz_guard_path_traversal_null_bytes_expected(name: str) -> None:
    """Fuzz guard_path_traversal with null bytes."""
    with pytest.raises((ValueError, TypeError, SecurityError)):
        guard_path_traversal(name, base_dir=Path("/safe_tmp"))
