from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import sanitize_filename, sanitize_path


@settings(max_examples=100)
@given(st.text(), st.integers(min_value=-1000, max_value=-1), st.text(), st.booleans())
def test_fuzz_sanitize_filename_negative_max_length_expected(
    filename: str, max_len: int, replacement: str, preserve: bool
) -> None:
    with pytest.raises((ValueError, TypeError)) as exc_info:
        sanitize_filename(
            filename,
            max_length=max_len,
            replacement=replacement,
            preserve_extension=preserve,
        )

    error_msg = str(exc_info.value)
    if isinstance(exc_info.value, ValueError):
        assert (
            "max_length cannot be negative" in error_msg
            or "Filename length exceeds maximum allowed limit" in error_msg
        )
    elif isinstance(exc_info.value, TypeError):
        assert "must be str" in error_msg


@settings(max_examples=100)
@given(
    st.one_of(st.text(), st.builds(Path, st.text())),
    st.one_of(st.none(), st.builds(Path, st.text())),
    st.integers(min_value=-1000, max_value=-1),
    st.booleans(),
)
def test_fuzz_sanitize_path_negative_max_depth_expected(
    path: str | Path, base_dir: Path | None, max_depth: int, resolve: bool
) -> None:
    with pytest.raises((ValueError, TypeError)) as exc_info:
        sanitize_path(path, base_dir=base_dir, max_depth=max_depth, resolve=resolve)

    error_msg = str(exc_info.value)
    if isinstance(exc_info.value, ValueError):
        assert (
            "max_depth cannot be negative" in error_msg
            or "Path length exceeds maximum allowed" in error_msg
            or "Cannot resolve path" in error_msg
        )
