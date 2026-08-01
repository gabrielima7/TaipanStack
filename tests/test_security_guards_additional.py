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
