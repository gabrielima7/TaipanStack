import pytest

from taipanstack.security.sanitizers import (
    MAX_PATH_LENGTH,
    sanitize_filename,
)


# Testing Massive Lengths (DoS) using simple parameters because Hypothesis
# has maximum string length limits around 65535 chars which aren't large enough.
def test_fuzz_sanitizers_dos_sanitize_filename_massive() -> None:
    filename = "a" * (MAX_PATH_LENGTH + 1)
    with pytest.raises(
        ValueError, match="Filename length exceeds maximum allowed limit"
    ):
        sanitize_filename(filename)


# Also test null bytes, as requested by instructions
