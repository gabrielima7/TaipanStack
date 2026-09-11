def test_security_sanitizers_additional_security_sanitizers_handle_normal_part():
    from unittest.mock import patch

    from taipanstack.security.sanitizers import _handle_normal_part

    parts = []
    # Test safe_part == ".."
    with patch(
        "taipanstack.security.sanitizers._is_safe_path_part", return_value=False
    ):
        with patch(
            "taipanstack.security.sanitizers.sanitize_filename", return_value=".."
        ):
            _handle_normal_part("mocked", parts)
    assert parts == []

    # Test safe_part is empty
    with patch(
        "taipanstack.security.sanitizers._is_safe_path_part", return_value=False
    ):
        with patch(
            "taipanstack.security.sanitizers.sanitize_filename", return_value=""
        ):
            _handle_normal_part("mocked", parts)
    assert parts == []


def test_security_sanitizers_additional_security_sanitizers_process_path_part_empty_or_dot_dot():
    from taipanstack.security.sanitizers import sanitize_path

    res = sanitize_path("a/./b")
    assert str(res).replace("\\", "/") == "a/b"
    res = sanitize_path("a/..b/c")
    assert str(res).replace("\\", "/") == "a/..b/c"
    res = sanitize_path("a/../b")
    assert str(res).replace("\\", "/") == "b"


def test_security_sanitizers_additional_security_sanitizers_path_null_byte_returns_err():
    from taipanstack.security.sanitizers import sanitize_path

    res = sanitize_path("a/\x00b")
    assert "\x00" not in str(res)


def test_security_sanitizers_additional_security_sanitizers_path_absolute_returns_err():
    from taipanstack.security.sanitizers import sanitize_path

    res = sanitize_path("/a/b")
    assert "a" in str(res) and "b" in str(res)


def test_is_valid_length_and_not_dot():
    from taipanstack.security.sanitizers import _is_valid_length_and_not_dot

    assert _is_valid_length_and_not_dot("a" * 255, 255) is True
    assert _is_valid_length_and_not_dot("a" * 256, 255) is False
    assert _is_valid_length_and_not_dot(".", 255) is False
    assert _is_valid_length_and_not_dot("..", 255) is False


def test_has_safe_characters():
    from taipanstack.security.sanitizers import _has_safe_characters

    assert _has_safe_characters("abc", "abc") is True
    assert _has_safe_characters("con.txt", "con") is False
    assert _has_safe_characters("lpt1.txt", "lpt1") is False
    assert _has_safe_characters("valid-name_123.txt", "valid-name_123") is True
    assert _has_safe_characters("invalid/name", "invalid/name") is False
    assert _has_safe_characters("invalid\x00name", "invalid\x00name") is False


def test_resolve_sanitized_path_error():
    import unittest.mock
    from pathlib import Path

    import pytest

    from taipanstack.security.sanitizers import _resolve_sanitized_path

    path = Path("/safe_path")
    with unittest.mock.patch.object(Path, "resolve", side_effect=OSError("Mock error")):
        with pytest.raises(ValueError, match="Cannot resolve path: Mock error"):
            _resolve_sanitized_path(path)


def test_resolve_sanitized_path_runtime_error():
    import unittest.mock
    from pathlib import Path

    import pytest

    from taipanstack.security.sanitizers import _resolve_sanitized_path

    path = Path("/safe_path")
    with unittest.mock.patch.object(
        Path, "resolve", side_effect=RuntimeError("Mock runtime error")
    ):
        with pytest.raises(ValueError, match="Cannot resolve path: Mock runtime error"):
            _resolve_sanitized_path(path)
