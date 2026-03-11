"""Main module for app."""

from taipanstack.utils.logging import get_logger, setup_logging

# Configure logging
setup_logging(level="INFO")
logger = get_logger(__name__)


def greet(name: str) -> str:
    """
    Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting message.

    """
    return f"Hello, {name}!"


def main() -> None:
    """Run the main entry point for the application."""
    message = greet("World")
    logger.info(message)


if __name__ == "__main__":
    main()
