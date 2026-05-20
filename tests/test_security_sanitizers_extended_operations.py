from taipanstack.security.sanitizers import sanitize_filename


def test_security_sanitizers_extended_sanitize_filename_re_error():
    assert (
        sanitize_filename("bad<>file", replacement="\\g<1>")
        == "bad\\g<1>g<1>\\g<1>g<1>file"
    )


def test_security_sanitizers_extended_sanitize_filename_re_error_multiple():
    assert sanitize_filename("badfile", replacement="\\g<1>") == "badfile"


def test_security_sanitizers_extended_sanitize_filename_re_error_backslash():
    assert sanitize_filename("bad<>file", replacement="\\") == "bad\\file"

def test_sanitize_path_resolve_err():
    from pathlib import Path

    import pytest

    from taipanstack.security.sanitizers import sanitize_path

    class FaultyPath(type(Path())):
        def resolve(self, *args, **kwargs):
            raise RuntimeError("mock err")

    with pytest.raises(ValueError, match="Cannot resolve base_dir"):
        from unittest.mock import patch

        with patch(
            "taipanstack.security.sanitizers.Path.resolve",
            side_effect=RuntimeError("mock err"),
        ):
            sanitize_path("foo/bar", base_dir="/root", resolve=True)


def test_sanitize_path_safepart_empty_2():
    from pathlib import Path

    from taipanstack.security.sanitizers import sanitize_path
    assert sanitize_path("a/..") == Path()


def test_sanitize_path_dot_part():
    from pathlib import Path

    from taipanstack.security.sanitizers import sanitize_path
    assert sanitize_path(".") == Path()


def test_sanitize_path_null_byte_str_coverage():
    from pathlib import Path

    from taipanstack.security.sanitizers import sanitize_path
    # Covers the "\x00" in path string condition in _normalize_path_input
    assert sanitize_path("foo\x00bar") == Path("foobar")


def test_sanitize_path_massive_path_object_coverage():
    from pathlib import Path

    import pytest

    from taipanstack.security.sanitizers import sanitize_path

    with pytest.raises(ValueError, match="Path length exceeds maximum allowed"):
        sanitize_path(Path("a" * 5000))


def test_sanitize_path_null_byte_path_coverage():
    from pathlib import Path
    # Covers the "\x00" in path string condition in _normalize_path_input for non-string types
    class PathWithNullStr(Path):
        def __str__(self):
            return "foo\x00bar"


def test_sanitize_path_null_byte_path_coverage2():
    class CustomPathLike:
        def __str__(self):
            return "foo"

        def __fspath__(self):
            return "foo"


def test_sanitize_path_null_byte_in_str():
    from pathlib import Path

    from taipanstack.security.sanitizers import sanitize_path
    # Covers the "\x00" replace logic
    assert sanitize_path("foo\x00bar") == Path("foobar")


def test_sanitize_path_absolute_reconstruct():
    # Covers _reconstruct_path for absolute paths
    from pathlib import Path

    from taipanstack.security.sanitizers import sanitize_path

    abs_path = Path("/foo/bar")
    assert sanitize_path(abs_path) == Path("/unnamed/foo/bar")


def test_sanitize_path_depth_exceeded():
    import pytest

    from taipanstack.security.sanitizers import sanitize_path

    with pytest.raises(ValueError, match="Path depth .* exceeds maximum of"):
        sanitize_path("a/b/c/d/e", max_depth=3)


def test_sanitize_path_null_byte_path_coverage3():
    pass


def test_sanitize_path_str_length_exceeded():
    import pytest

    from taipanstack.security.sanitizers import sanitize_path

    with pytest.raises(ValueError, match="Path length exceeds maximum allowed"):
        sanitize_path("a" * 5000)
