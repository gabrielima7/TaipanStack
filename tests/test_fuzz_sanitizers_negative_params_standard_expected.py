import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pathlib import Path

from taipanstack.security.sanitizers import sanitize_filename, sanitize_path


@settings(max_examples=100)
@given(st.text(), st.integers(min_value=-1000, max_value=-1), st.text(), st.booleans())
def test_fuzz_sanitize_filename_negative_max_length_standard_expected(
    filename: str, max_len: int, replacement: str, preserve: bool
) -> None:
    try:
        sanitize_filename(
            filename,
            max_length=max_len,
            replacement=replacement,
            preserve_extension=preserve,
        )
    except Exception as e:
        assert isinstance(e, (ValueError, TypeError))
        if isinstance(e, ValueError) and "max_length cannot be negative" in str(e):
            pass
        elif isinstance(e, TypeError) and "must be str" in str(e):
            pass
        elif isinstance(
            e, ValueError
        ) and "Filename length exceeds maximum allowed limit" in str(e):
            pass
        else:
            pytest.fail(f"Unexpected exception: {type(e)} {e}")


@settings(max_examples=100)
@given(
    st.one_of(st.text(), st.builds(Path, st.text())),
    st.one_of(st.none(), st.builds(Path, st.text())),
    st.integers(min_value=-1000, max_value=-1),
    st.booleans(),
)
def test_fuzz_sanitize_path_negative_max_depth_standard_expected(
    path, base_dir, max_depth: int, resolve: bool
) -> None:
    try:
        sanitize_path(path, base_dir=base_dir, max_depth=max_depth, resolve=resolve)
    except Exception as e:
        assert isinstance(e, (ValueError, TypeError))
        if isinstance(e, ValueError) and "max_depth cannot be negative" in str(e):
            pass
        elif isinstance(e, ValueError) and (
            "Path length exceeds maximum allowed" in str(e)
            or "Cannot resolve path" in str(e)
        ):
            pass
        else:
            pytest.fail(f"Unexpected exception: {type(e)} {e}")
