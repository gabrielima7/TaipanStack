from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

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
        error_msg = str(e)
        if isinstance(e, ValueError) and (
            "max_length cannot be negative" in error_msg
            or "Filename length exceeds maximum allowed limit" in error_msg
        ):
            return
        if isinstance(e, TypeError) and "must be str" in error_msg:
            return
        pytest.fail(f"Unexpected exception: {type(e)} {e}")


@settings(max_examples=100)
@given(
    st.one_of(st.text(), st.builds(Path, st.text())),
    st.one_of(st.none(), st.builds(Path, st.text())),
    st.integers(min_value=-1000, max_value=-1),
    st.booleans(),
)
def test_fuzz_sanitize_path_negative_max_depth_standard_expected(
    path: str | Path, base_dir: Path | None, max_depth: int, resolve: bool
) -> None:
    try:
        sanitize_path(path, base_dir=base_dir, max_depth=max_depth, resolve=resolve)
    except Exception as e:
        error_msg = str(e)
        if isinstance(e, ValueError) and (
            "max_depth cannot be negative" in error_msg
            or "Path length exceeds maximum allowed" in error_msg
            or "Cannot resolve path" in error_msg
        ):
            return
        if isinstance(e, TypeError):
            return
        pytest.fail(f"Unexpected exception: {type(e)} {e}")
