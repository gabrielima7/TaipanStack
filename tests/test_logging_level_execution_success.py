from taipanstack.utils.logging import _configure_structlog


def test_configure_structlog_level_string_execution_success():
    _configure_structlog(level="DEBUG")


def test_configure_structlog_level_int_execution_success():
    import logging

    _configure_structlog(level=logging.WARNING)
