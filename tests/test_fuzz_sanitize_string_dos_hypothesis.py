import pytest

from taipanstack.security.sanitizers import MAX_STRING_LENGTH, sanitize_string


def test_fuzz_sanitize_string_dos_hypothesis_fuzz_sanitize_string_dos_hypothesis() -> (
    None
):
    # Generate a string larger than MAX_STRING_LENGTH to trigger ValueError
    value = "a" * (MAX_STRING_LENGTH + 1)

    with pytest.raises(ValueError, match="String length exceeds maximum allowed"):
        sanitize_string(value)
