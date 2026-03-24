import pytest
import os
import sys

def test_sanitize_filename_coverage():
    from taipanstack.security.sanitizers import sanitize_filename
    orig_name = os.name
    # Simulate nt path
    os.name = "nt"
    try:
        assert sanitize_filename("a\\b") == "b"
        assert sanitize_filename("\\") == "unnamed"
    finally:
        os.name = orig_name

    # Simulate non-nt path
    os.name = "posix"
    try:
        assert sanitize_filename("a/b") == "b"
        assert sanitize_filename("\\") == "unnamed"
    finally:
        os.name = orig_name
