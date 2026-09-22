import hypothesis.strategies as st
from hypothesis import HealthCheck, given, settings

from taipanstack.security.guards import SecurityError, guard_file_extension


@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
@given(
    st.text(),
    st.one_of(st.none(), st.lists(st.text()), st.text(), st.integers()),
    st.one_of(st.none(), st.lists(st.text()), st.text(), st.integers()),
)
def test_fuzz_guard_file_extension_comprehensive(filename, allowed, denied):
    try:
        guard_file_extension(
            filename, allowed_extensions=allowed, denied_extensions=denied
        )
    except (TypeError, ValueError, SecurityError):
        pass
    except Exception as e:
        # If it's a completely unexpected exception, bubble it up
        if (
            "maximum recursion depth" not in str(e).lower()
            and "memory" not in str(e).lower()
        ):
            raise
