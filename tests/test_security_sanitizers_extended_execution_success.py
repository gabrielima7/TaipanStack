from taipanstack.security.sanitizers import sanitize_filename


def test_security_sanitizers_extended_sanitize_filename_re_error_execution_success():
    assert (
        sanitize_filename("bad<>file", replacement="\\g<1>")
        == "bad\\g<1>g<1>\\g<1>g<1>file"
    )


def test_security_sanitizers_extended_sanitize_filename_re_error_multiple_execution_success():
    assert sanitize_filename("badfile", replacement="\\g<1>") == "badfile"


def test_security_sanitizers_extended_sanitize_filename_re_error_backslash_execution_success():
    assert sanitize_filename("bad<>file", replacement="\\") == "bad\\file"
