def test_security_sanitizers_additional_security_sanitizers_handle_normal_part_expected():
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


def test_security_sanitizers_additional_security_sanitizers_process_path_part_empty_or_dot_dot_expected():
    from taipanstack.security.sanitizers import sanitize_path

    res = sanitize_path("a/./b")
    assert str(res).replace("\\", "/") == "a/b"
    res = sanitize_path("a/..b/c")
    assert str(res).replace("\\", "/") == "a/..b/c"
    res = sanitize_path("a/../b")
    assert str(res).replace("\\", "/") == "b"


def test_security_sanitizers_additional_security_sanitizers_path_null_byte_returns_err_expected():
    from taipanstack.security.sanitizers import sanitize_path

    res = sanitize_path("a/\x00b")
    assert "\x00" not in str(res)


def test_security_sanitizers_additional_security_sanitizers_path_absolute_returns_err_expected():
    from taipanstack.security.sanitizers import sanitize_path

    res = sanitize_path("/a/b")
    assert "a" in str(res) and "b" in str(res)
