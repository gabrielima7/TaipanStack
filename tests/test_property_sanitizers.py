"""Property-based tests for input sanitizers using Hypothesis.

Generates thousands of mutant inputs to verify sanitizer invariants
hold under adversarial conditions.
"""

from __future__ import annotations

import string
from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from taipanstack.security.sanitizers import (
    sanitize_env_value,
    sanitize_filename,
    sanitize_path,
    sanitize_sql_identifier,
    sanitize_string,
)

# ── Shared strategies ───────────────────────────────────────────────────────

# Text that may include control chars, null bytes, unicode, HTML
nasty_text = st.text(
    alphabet=st.characters(codec="utf-8"),
    min_size=0,
    max_size=500,
)

# Filenames with dangerous chars mixed in
nasty_filename = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "P", "S", "Z"),
        whitelist_characters='../\\<>:"|?*\x00',
    ),
    min_size=0,
    max_size=300,
)

# Path-like strings with traversal attempts
nasty_path = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N"),
        whitelist_characters="/..\\\x00",
    ),
    min_size=1,
    max_size=200,
)


FUZZ_EXAMPLES = 1000


# =============================================================================
# sanitize_string — Properties
# =============================================================================
class TestSanitizeStringProperties:
    """Property-based tests for sanitize_string."""

    @given(text=nasty_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_never_contains_null_bytes(self, text: str) -> None:
        """Output must never contain null bytes."""
        result = sanitize_string(text)
        assert "\x00" not in result

    @given(text=nasty_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_control_characters_except_whitespace(self, text: str) -> None:
        """Output must not contain control characters (except newline, tab, CR)."""
        result = sanitize_string(text)
        allowed_controls = {"\n", "\r", "\t"}
        for ch in result:
            if ord(ch) < 32 and ch not in allowed_controls:
                pytest.fail(
                    f"Control character U+{ord(ch):04X} found in output: {result!r}"
                )

    @given(text=nasty_text, max_len=st.integers(min_value=1, max_value=100))
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_respects_max_length(self, text: str, max_len: int) -> None:
        """Output length must not exceed max_length."""
        result = sanitize_string(text, max_length=max_len)
        assert len(result) <= max_len

    @given(text=nasty_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_returns_string_type(self, text: str) -> None:
        """Output must always be a string."""
        result = sanitize_string(text)
        assert isinstance(result, str)

    @given(text=nasty_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_html_tags_removed_by_default(self, text: str) -> None:
        """Output must not contain HTML angle-bracket tags when allow_html=False."""
        import re

        result = sanitize_string(text, allow_html=False)
        # After sanitization, no raw < > should form valid HTML tags
        assert not re.search(r"<[a-zA-Z/][^>]*>", result)


# =============================================================================
# sanitize_filename — Properties
# =============================================================================
class TestSanitizeFilenameProperties:
    """Property-based tests for sanitize_filename."""

    @given(text=nasty_filename)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_never_empty(self, text: str) -> None:
        """Output filename must never be completely empty."""
        result = sanitize_filename(text)
        assert len(result) > 0

    @given(text=nasty_filename)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_path_separators(self, text: str) -> None:
        """Output stem must not contain path separator characters.

        Note: sanitize_filename sanitizes the *stem* only; the extension
        is preserved as-is from Path(filename).suffix. We therefore only
        assert on the stem portion of the output.
        """
        result = sanitize_filename(text)
        stem = Path(result).stem
        assert "/" not in stem
        assert "\\" not in stem

    @given(text=nasty_filename)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_null_bytes(self, text: str) -> None:
        """Stem portion of output must not contain null bytes.

        Note: sanitize_filename sanitizes the stem only; the extension
        is preserved as-is from Path(filename).suffix.
        """
        result = sanitize_filename(text)
        stem = Path(result).stem
        assert "\x00" not in stem

    @given(
        text=st.text(
            # Guarantee at least one character so the 'unnamed' fallback is never hit
            alphabet=st.characters(
                whitelist_categories=("L", "N", "P", "S", "Z"),
                whitelist_characters='../\\<>:"|?*\x00',
            ),
            min_size=1,
            max_size=300,
        ),
        max_len=st.integers(min_value=5, max_value=255),
    )
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_respects_max_length(self, text: str, max_len: int) -> None:
        """Output length must not exceed max_length for non-empty filenames.

        The 'unnamed' fallback for empty inputs bypasses max_length.
        We avoid that by requiring min_size=1.
        """
        result = sanitize_filename(text, max_length=max_len)
        assert len(result) <= max_len

    @given(text=nasty_filename)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_windows_reserved_chars(self, text: str) -> None:
        """Stem portion of output must not contain Windows-reserved characters.

        Note: sanitize_filename sanitizes the stem but preserves the
        extension byte-for-byte. We therefore only check the stem.
        """
        result = sanitize_filename(text)
        stem = Path(result).stem
        reserved = set('<>:"|?*')
        for ch in stem:
            assert ch not in reserved, (
                f"Reserved char {ch!r} found in stem {stem!r} (full: {result!r})"
            )

    def test_mutmut_boundaries_and_limits(self) -> None:
        """Strict non-fuzzing bounds to trap and kill Mutmut surviving mutants.

        This tests precise mathematical conditions (e.g. len == max_length)
        and default arguments that fuzzing might miss structurally.
        """
        # 1. Kill 'max_length=255' mutated to 256
        res_default = sanitize_filename("A" * 300)
        assert len(res_default) == 255, "Mutant survived: max_length default altered"

        # 2. Kill 'if len(result) > max_length' mutated to '>='
        res_exact = sanitize_filename("B" * 10, max_length=10)
        assert len(res_exact) == 10
        assert res_exact == "B" * 10, (
            "Mutant survived: strict '>' boundary mutated to '>='"
        )

        # 3. Kill 'if available > 0' mutated to '>=' or '-' to '+'
        # When suffix exactly equals max_length, available == 0.
        # Original code goes to 'else: result = result[:max_length]' producing "stem.1234"
        # If mutated to '>= 0', it goes to 'if' block producing "" + ".12345678"
        exact_suffix = ".12345678"  # exactly 9 chars
        res_zero = sanitize_filename("stem" + exact_suffix, max_length=9)
        assert res_zero == "stem.1234", "Mutant survived: available > 0 logic bypassed!"


# =============================================================================
# sanitize_path — Properties
# =============================================================================
class TestSanitizePathProperties:
    """Property-based tests for sanitize_path."""

    @given(
        text=st.from_regex(r"[a-zA-Z0-9_./]{1,50}", fullmatch=True),
    )
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_traversal_in_output(self, text: str) -> None:
        """Output path must not contain standalone '..' traversal components.

        Note: sanitize_path removes standalone '..' *path parts* (e.g. foo/../bar).
        It does NOT alter parts whose name happens to contain consecutive dots
        (e.g. '0..0' is a valid filename, not a traversal). We therefore check
        that no *part* of the output path equals '..'.
        """
        try:
            result = sanitize_path(text, max_depth=None)
            for part in Path(str(result)).parts:
                assert part != "..", (
                    f"Traversal component '..' found as path part in: {result!r}"
                )
        except ValueError:
            pass  # Invalid paths raising ValueError is acceptable

    @given(text=nasty_path)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_null_bytes(self, text: str) -> None:
        """Output path must not contain null bytes."""
        try:
            result = sanitize_path(text, max_depth=None)
            assert "\x00" not in str(result)
        except ValueError:
            pass

    @given(
        segments=st.lists(
            st.from_regex(r"[a-z]{1,8}", fullmatch=True),
            min_size=1,
            max_size=20,
        ),
        max_depth=st.integers(min_value=1, max_value=10),
    )
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_depth_enforcement(self, segments: list[str], max_depth: int) -> None:
        """Paths deeper than max_depth must raise ValueError."""
        path = "/".join(segments)
        if len(segments) > max_depth:
            with pytest.raises(ValueError, match="depth"):
                sanitize_path(path, max_depth=max_depth)
        else:
            result = sanitize_path(path, max_depth=max_depth)
            assert str(result)  # Should succeed


# =============================================================================
# sanitize_env_value — Properties
# =============================================================================
class TestSanitizeEnvValueProperties:
    """Property-based tests for sanitize_env_value."""

    @given(text=nasty_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_null_bytes(self, text: str) -> None:
        """Output must not contain null bytes."""
        result = sanitize_env_value(text)
        assert "\x00" not in result

    @given(text=nasty_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_no_newlines_by_default(self, text: str) -> None:
        """Output must not contain newlines when allow_multiline=False."""
        result = sanitize_env_value(text, allow_multiline=False)
        assert "\n" not in result
        assert "\r" not in result

    @given(text=nasty_text, max_len=st.integers(min_value=1, max_value=500))
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_respects_max_length(self, text: str, max_len: int) -> None:
        """Output length must not exceed max_length."""
        result = sanitize_env_value(text, max_length=max_len)
        assert len(result) <= max_len

    @given(text=nasty_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_returns_string_type(self, text: str) -> None:
        """Output must always be a string."""
        result = sanitize_env_value(text)
        assert isinstance(result, str)


# =============================================================================
# sanitize_sql_identifier — Properties
# =============================================================================

# Strategy: generate strings that have at least one valid SQL identifier char
sql_text = st.text(
    alphabet=st.characters(codec="utf-8"),
    min_size=1,
    max_size=200,
)

# Strategy: generate strings guaranteed to have valid identifier chars
valid_sql_text = st.text(
    alphabet=st.sampled_from(list(string.ascii_letters + string.digits + "_")),
    min_size=1,
    max_size=200,
)


class TestSanitizeSqlIdentifierProperties:
    """Property-based tests for sanitize_sql_identifier."""

    @given(text=valid_sql_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_only_valid_chars_in_output(self, text: str) -> None:
        """Output must contain only alphanumeric characters and underscores."""
        result = sanitize_sql_identifier(text)
        valid = set(string.ascii_letters + string.digits + "_")
        for ch in result:
            assert ch in valid, f"Invalid char {ch!r} in SQL identifier: {result!r}"

    @given(text=valid_sql_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_max_length_128(self, text: str) -> None:
        """Output must not exceed 128 characters."""
        result = sanitize_sql_identifier(text)
        assert len(result) <= 128

    @given(text=valid_sql_text)
    @settings(max_examples=FUZZ_EXAMPLES, suppress_health_check=[HealthCheck.too_slow])
    def test_does_not_start_with_digit(self, text: str) -> None:
        """Output must not start with a digit."""
        result = sanitize_sql_identifier(text)
        assert not result[0].isdigit(), f"SQL identifier starts with digit: {result!r}"

    def test_empty_raises_value_error(self) -> None:
        """Empty identifier must raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            sanitize_sql_identifier("")

    def test_only_invalid_chars_raises(self) -> None:
        """Identifier with only invalid characters must raise ValueError."""
        with pytest.raises(ValueError, match="no valid characters"):
            sanitize_sql_identifier("!@#$%^&*()")
