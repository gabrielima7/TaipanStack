import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import SecurityError, guard_file_extension


@settings(max_examples=200)
@given(st.text())
def test_fuzz_guard_file_extension_null_bytes_expected(filename: str) -> None:
    """Ensure filenames with null bytes are rejected."""
    if "\x00" in filename:
        with pytest.raises(SecurityError, match="null byte"):
            guard_file_extension(filename, denied_extensions=["exe"])


@settings(max_examples=200)
@given(
    st.text(
        alphabet=st.characters(
            whitelist_categories=("Z", "C"), whitelist_characters=[".", " ", "\xad"]
        ),
        min_size=1,
        max_size=10,
    )
)
def test_fuzz_guard_file_extension_whitespace_and_dots_expected(padding: str) -> None:
    """Ensure trailing spaces, dots, and control characters don't bypass the extension check."""
    # We want to catch Windows-style bypasses like 'test.exe.' or 'test.exe \n'
    # padding only contains whitespace, control chars, or dots
    filename = f"test.exe{padding}"

    # \x00 should raise null byte error
    if "\x00" in padding:
        with pytest.raises(SecurityError, match="null byte"):
            guard_file_extension(filename, denied_extensions=["exe"])
    else:
        # It should detect 'exe' as the extension and reject it
        with pytest.raises(SecurityError, match="not allowed"):
            guard_file_extension(filename, denied_extensions=["exe"])


def test_fuzz_guard_file_extension_empty_after_strip_expected() -> None:
    """Ensure that filenames that become empty after stripping are handled correctly."""
    with pytest.raises(SecurityError, match="not in allowed list"):
        guard_file_extension("   \\xad", allowed_extensions=["txt"])


def test_fuzz_guard_file_extension_empty_name_expected() -> None:
    """Ensure that filenames with no name component are handled."""
    with pytest.raises(SecurityError, match="not in allowed list"):
        guard_file_extension("/", allowed_extensions=["txt"])
