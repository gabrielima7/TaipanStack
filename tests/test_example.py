"""Example test module for app."""

from app.main import greet


def test_example_greet_expected() -> None:
    """Test the greet function."""
    result = greet("Alice")
    assert result == "Hello, Alice!"
    assert isinstance(result, str)


def test_example_greet_empty_expected() -> None:
    """Test greet with empty string."""
    result = greet("")
    assert result == "Hello, !"
