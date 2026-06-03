from pathlib import Path

import pytest


def test_security_guards_additional_security_guards_path_traversal_os_error_symlink():
    from unittest.mock import patch

    from taipanstack.security.guards import SecurityError, guard_path_traversal

    with patch("pathlib.Path.is_symlink", side_effect=OSError("mocked oserror")):
        with pytest.raises(SecurityError):
            guard_path_traversal("some/path", Path("/safe_tmp"))


def test_security_guards_additional_security_guards_file_extension_none_allowed():
    from taipanstack.security.guards import guard_file_extension

    result = guard_file_extension("file.txt", allowed_extensions=None)
    assert result == Path("file.txt")


def test_security_guards_additional_security_guards_ssrf_control_characters():
    from taipanstack.core.result import Err
    from taipanstack.security.guards import guard_ssrf

    # Null byte bypass
    res = guard_ssrf("http://127.0.0.1\x00@google.com")
    assert isinstance(res, Err)
    assert "URL contains invalid control characters or spaces" in str(res.err_value)

    # CRLF bypass
    res2 = guard_ssrf("http://127.0.0.1\r\n@google.com")
    assert isinstance(res2, Err)
    assert "URL contains invalid control characters or spaces" in str(res2.err_value)

    # Space bypass
    res3 = guard_ssrf("http://127.0.0.1 @google.com")
    assert isinstance(res3, Err)
    assert "URL contains invalid control characters or spaces" in str(res3.err_value)
