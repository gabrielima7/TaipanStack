from pathlib import Path

import pytest

from taipanstack.core.result import Err
from taipanstack.security.guards import SecurityError, guard_ssrf


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


def test_security_guards_ssrf_obfuscated_hostname():
    url = "http://127.0.0.1\\@example.com"
    result = guard_ssrf(url)
    assert isinstance(result, Err)
    assert isinstance(result.unwrap_err(), SecurityError)
    assert "obfuscated characters" in result.unwrap_err().args[0]


def test_security_guards_ssrf_obfuscated_hostname_at():
    url2 = "http://user@127.0.0.1:80\\@example.com"
    result = guard_ssrf(url2)
    assert isinstance(result, Err)
    assert isinstance(result.unwrap_err(), SecurityError)

def test_security_guards_command_injection_non_string():
    from taipanstack.security.guards import guard_command_injection
    with pytest.raises(TypeError):
        guard_command_injection(["ls", 123])

def test_security_guards_ssrf_malformed_url():
    from taipanstack.security.guards import guard_ssrf
    # Using a malformed port representation which causes ValueError in urlsplit
    result = guard_ssrf("http://]")
    assert isinstance(result, Err)
    assert isinstance(result.unwrap_err(), SecurityError)
    assert "Malformed URL:" in result.unwrap_err().args[0]
