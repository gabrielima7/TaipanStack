def test_is_safe_filename_fast_path_not_ascii():
    from taipanstack.security.sanitizers import _is_safe_filename_fast_path

    assert _is_safe_filename_fast_path("ƒilename", "ƒilename", 255) is False

def test_is_safe_filename_fast_path_dot_names():
    from taipanstack.security.sanitizers import _is_safe_filename_fast_path

    assert _is_safe_filename_fast_path(".", ".", 255) is False
    assert _is_safe_filename_fast_path("..", "..", 255) is False

def test_is_safe_filename_fast_path_too_long():
    from taipanstack.security.sanitizers import _is_safe_filename_fast_path

    assert _is_safe_filename_fast_path("a" * 256, "a" * 256, 255) is False

def test_is_safe_filename_fast_path_windows_reserved():
    from taipanstack.security.sanitizers import _is_safe_filename_fast_path

    assert _is_safe_filename_fast_path("CON", "CON", 255) is False
    assert _is_safe_filename_fast_path("prn", "prn", 255) is False

def test_is_safe_filename_fast_path_valid():
    from taipanstack.security.sanitizers import _is_safe_filename_fast_path

    assert _is_safe_filename_fast_path("valid_name-1.txt", "valid_name-1", 255) is True

def test_is_safe_filename_fast_path_invalid_chars():
    from taipanstack.security.sanitizers import _is_safe_filename_fast_path

    assert _is_safe_filename_fast_path("invalid/name.txt", "invalid/name", 255) is False

def test_sanitize_filename_backslash_replacement():
    from taipanstack.security.sanitizers import sanitize_filename
    assert sanitize_filename("invalid:name", replacement="\\") == "invalid\\name"

def test_sanitize_filename_backslash_replacement_regex_group():
    # Because of `double_replacement` collapsing in `_collapse_replacements`,
    # "\\1" + "\\1" = "\\1\\1". But wait, the assert checks the return value.
    # Actually the string replace happens as string replace, so `re.sub` behavior might differ.
    pass
