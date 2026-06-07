"""Tests for app.main module."""

from unittest.mock import patch

from app.main import greet, main


def test_app_main_greet_standard_expected() -> None:
    """Test the greet function with various inputs."""
    assert greet("World") == "Hello, World!"
    assert greet("Alice") == "Hello, Alice!"
    assert greet("") == "Hello, !"


def test_app_main_main_standard_expected() -> None:
    """Test the main function and verify logging."""
    with patch("app.main.logger") as mock_logger:
        main()
        # main() calls greet("World"), which returns "Hello, World!"
        mock_logger.info.assert_called_once_with("Hello, World!")
