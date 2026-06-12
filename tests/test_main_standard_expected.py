"""Tests for the main app module."""

import logging

import pytest

from app.main import greet, main


def test_main_greet_standard_expected() -> None:
    """Test greet function returns expected format."""
    assert greet("Alice") == "Hello, Alice!"


def test_main_function_logs_standard_expected(caplog: pytest.LogCaptureFixture) -> None:
    """Test that main function logs the greeting."""
    with caplog.at_level(logging.INFO):
        main()
    assert "Hello, World!" in caplog.text
