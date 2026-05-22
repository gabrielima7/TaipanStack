import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.guards import SecurityError, guard_file_extension


@settings(max_examples=200)
@given(st.text())
def test_fuzz_guard_file_extension_null_bytes(filename: str) -> None:
    """Ensure filenames with null bytes are rejected."""
    if len(filename) > 4096:
        with pytest.raises(SecurityError, match="Filename length exceeds"):
            guard_file_extension(filename, denied_extensions=["exe"])
        return

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
def test_fuzz_guard_file_extension_whitespace_and_dots(padding: str) -> None:
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


def test_fuzz_guard_file_extension_empty_after_strip() -> None:
    """Ensure that filenames that become empty after stripping are handled correctly."""
    with pytest.raises(SecurityError, match="not in allowed list"):
        guard_file_extension("   \\xad", allowed_extensions=["txt"])


def test_fuzz_guard_file_extension_empty_name() -> None:
    """Ensure that filenames with no name component are handled."""
    with pytest.raises(SecurityError, match="not in allowed list"):
        guard_file_extension("/", allowed_extensions=["txt"])


@settings(
    suppress_health_check=[
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
        HealthCheck.too_slow,
    ],
    max_examples=2,
    deadline=None,
)
@given(st.text(min_size=4097, max_size=4099))
def test_fuzz_guard_file_extension_massive_strings_dos_property(
    ext: str,
) -> None:
    """Fuzz guard_file_extension with massive strings property test to ensure DoS protection limits are active."""
    with pytest.raises(
        SecurityError, match="Filename length exceeds maximum allowed limit"
    ):
        guard_file_extension(f"file.{ext}")


def test_fuzz_guard_file_extension_massive_strings_dos() -> None:
    """Fuzz guard_file_extension with massive strings to ensure DoS protection limits are active."""
    ext = "a" * 50000
    with pytest.raises(
        SecurityError, match="Filename length exceeds maximum allowed limit"
    ):
        guard_file_extension(f"file.{ext}")
