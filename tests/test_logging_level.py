from taipanstack.utils.logging import _configure_structlog


def test_logging_level_configure_structlog_level_string():
    _configure_structlog(level="DEBUG")


def test_logging_level_configure_structlog_level_int():
    import logging

    _configure_structlog(level=logging.WARNING)
