"""Tests for app.main module."""

from unittest.mock import patch

from app.main import greet, main


def test_greet() -> None:
    """Test the greet function with various inputs."""
    assert greet("World") == "Hello, World!"
    assert greet("Alice") == "Hello, Alice!"
    assert greet("") == "Hello, !"


def test_main() -> None:
    """Test the main function and verify logging."""
    with patch("app.main.logger") as mock_logger:
        main()
        # main() calls greet("World"), which returns "Hello, World!"
        mock_logger.info.assert_called_once_with("Hello, World!")


class TestAppMain:
    """Tests for app/main.py uncovered lines 26-27."""

    def test_main_function(self) -> None:
        """Test main() function execution."""
        import structlog
        from structlog.testing import capture_logs

        # Because `logger` is created at module import, we must patch its backend
        import app.main
        from app.main import main

        with capture_logs() as cap_logs:
            # Re-bind the logger so it uses the captured logs
            app.main.logger = structlog.get_logger("app.main")
            main()

        assert any("Hello, World!" in event["event"] for event in cap_logs)
