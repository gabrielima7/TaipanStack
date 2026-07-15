"""Tests for the main app module."""

import logging

import pytest

from app.main import greet, main


def test_main_greet_returns_hello_string() -> None:
    """Test greet function returns expected format."""
    assert greet("Alice") == "Hello, Alice!"


def test_main_function_logs(caplog: pytest.LogCaptureFixture) -> None:
    """Test that main function logs the greeting."""
    with caplog.at_level(logging.INFO):
        main()
    assert "Hello, World!" in caplog.text
