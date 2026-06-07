from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import SecurityError, guard_path_traversal


@settings(max_examples=1000)
@given(
    path=st.one_of(st.text(), st.binary(), st.integers()),
    base_dir=st.one_of(st.none(), st.text(), st.binary()),
    allow_symlinks=st.booleans(),
)
def test_fuzz_path_traversal_fuzz_guard_path_traversal_standard_expected(path, base_dir, allow_symlinks):
    # Fuzzing produces both valid and invalid inputs.
    # When input is invalid, it must raise SecurityError or TypeError.
    # When input is valid, it must return a Path.

    raised = False
    try:
        result = guard_path_traversal(
            path, base_dir=base_dir, allow_symlinks=allow_symlinks
        )
    except (SecurityError, TypeError):
        raised = True

    if not raised:
        assert isinstance(result, Path)
