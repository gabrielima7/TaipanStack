import importlib
import sys
from unittest.mock import patch


def test_v034_logging_coverage_coverage_expected():
    import taipanstack.utils.logging as my_logging

    old_regex = my_logging._SENSITIVE_KEY_REGEX
    my_logging._SENSITIVE_KEY_REGEX = None

    try:
        res = my_logging.mask_sensitive_data_processor(None, None, {"test": "val"})
        assert res == {"test": "val"}

        assert my_logging._is_sensitive("any", None) is False
    finally:
        my_logging._SENSITIVE_KEY_REGEX = old_regex


def test_v034_logging_import_error_expected():
    original_structlog = sys.modules.get("structlog")
    try:
        if "structlog" in sys.modules:
            del sys.modules["structlog"]
        with patch.dict(sys.modules, {"structlog": None}):
            if "taipanstack.utils.logging" in sys.modules:
                del sys.modules["taipanstack.utils.logging"]
            import taipanstack.utils.logging as l

            importlib.reload(l)
            assert l.HAS_STRUCTLOG is False
    finally:
        if original_structlog is not None:
            sys.modules["structlog"] = original_structlog
        elif "structlog" in sys.modules:
            del sys.modules["structlog"]


def test_is_sensitive_not_string_expected():
    import taipanstack.utils.logging as l

    assert l._is_sensitive(123, l._SENSITIVE_KEY_REGEX) is False
