from taipanstack.utils.logging import _configure_structlog


def test_configure_structlog_level_string_standard_expected():
    _configure_structlog(level="DEBUG")


def test_configure_structlog_level_int_standard_expected():
    import logging

    _configure_structlog(level=logging.WARNING)
