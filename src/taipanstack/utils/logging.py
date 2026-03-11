"""
Structured logging with context.

Provides a configured logger with support for structured output,
context propagation, and proper formatting.
"""

import logging
import re
import sys
from collections.abc import MutableMapping
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any, Literal

try:
    import structlog

    HAS_STRUCTLOG = True
except ImportError:  # pragma: no cover — structlog is optional
    HAS_STRUCTLOG = False


# Default log format
DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
JSON_FORMAT = (
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
    '"logger": "%(name)s", "message": "%(message)s"}'
)

SENSITIVE_KEY_PATTERNS: tuple[str, ...] = (
    "password",
    "secret",
    "token",
    "authorization",
    "api_key",
)

# Pre-compile the regex for O(1) checks per key instead of O(N*M)
_SENSITIVE_KEY_REGEX = (
    re.compile("|".join(map(re.escape, SENSITIVE_KEY_PATTERNS)), re.IGNORECASE)
    if SENSITIVE_KEY_PATTERNS
    else None
)

REDACTED_VALUE = "***REDACTED***"


def mask_sensitive_data_processor(
    logger: Any,  # noqa: ARG001
    method: str,  # noqa: ARG001
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    """Mask sensitive data in structlog event dictionaries.

    Intercept the *event_dict* produced by structlog and replace the
    value of any key whose name contains a sensitive substring with
    ``"***REDACTED***"``.  Matching is case-insensitive.

    Args:
        logger: The wrapped logger object (unused, required by structlog).
        method: The name of the log method called (unused, required by structlog).
        event_dict: The structured event dictionary.

    Returns:
        The event dictionary with sensitive values masked.

    """
    if _SENSITIVE_KEY_REGEX is None:
        return event_dict

    for key in event_dict:
        if _SENSITIVE_KEY_REGEX.search(key):
            event_dict[key] = REDACTED_VALUE
    return event_dict


# Context variables for observability
correlation_id_var: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)


def get_correlation_id() -> str | None:
    """Get the current correlation ID.

    Returns:
        The correlation ID if set, otherwise None.

    """
    return correlation_id_var.get()


def set_correlation_id(correlation_id: str | None) -> None:
    """Set the correlation ID for the current context.

    Args:
        correlation_id: The correlation ID string, or None to clear.

    """
    correlation_id_var.set(correlation_id)


def correlation_id_processor(
    logger: Any,  # noqa: ARG001
    method: str,  # noqa: ARG001
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    """Structlog processor to inject correlation ID into events.

    Args:
        logger: The wrapped logger object.
        method: The name of the log method called.
        event_dict: The structured event dictionary.

    Returns:
        The event dictionary with correlation_id injected if sets.

    """
    correlation_id = get_correlation_id()
    if correlation_id is not None:
        event_dict["correlation_id"] = correlation_id
    return event_dict


class StackLogger:
    """Enhanced logger with context support.

    Provides a wrapper around standard logging with additional features
    like context propagation and structured output support.

    Attributes:
        name: Logger name.
        level: Current log level.

    """

    def __init__(
        self,
        name: str = "stack",
        level: str = "INFO",
        *,
        use_structured: bool = False,
    ) -> None:
        """Initialize the logger.

        Args:
            name: Logger name.
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            use_structured: Use structured logging if structlog is available.

        """
        self.name = name
        self.level = level
        self._context: dict[str, Any] = {}

        if use_structured and HAS_STRUCTLOG:
            self._logger = structlog.get_logger(name)
            self._structured = True
        else:
            self._logger = logging.getLogger(name)
            self._logger.setLevel(getattr(logging, level.upper()))
            self._structured = False

    def bind(self, **context: Any) -> "StackLogger":
        """Add context to logger.

        Args:
            **context: Key-value pairs to add to context.

        Returns:
            Self for chaining.

        """
        self._context.update(context)
        if self._structured and HAS_STRUCTLOG:
            self._logger = self._logger.bind(**context)
        return self

    def unbind(self, *keys: str) -> "StackLogger":
        """Remove context keys.

        Args:
            *keys: Keys to remove from context.

        Returns:
            Self for chaining.

        """
        for key in keys:
            self._context.pop(key, None)
        if self._structured and HAS_STRUCTLOG:
            self._logger = self._logger.unbind(*keys)
        return self

    def _format_message(self, message: str, **kwargs: Any) -> str:
        """Format message with context.

        Args:
            message: The log message.
            **kwargs: Additional context for this message.

        Returns:
            Formatted message string.

        """
        if not kwargs and not self._context:
            return message

        context = {**self._context, **kwargs}
        if _SENSITIVE_KEY_REGEX is not None:
            for key in context:
                if _SENSITIVE_KEY_REGEX.search(key):
                    context[key] = REDACTED_VALUE
        context_str = " ".join(f"{k}={v}" for k, v in context.items())
        return f"{message} | {context_str}"

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message.

        Args:
            message: The message to log.
            **kwargs: Additional context.

        """
        if self._structured:
            self._logger.debug(message, **kwargs)
        else:
            self._logger.debug(self._format_message(message, **kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message.

        Args:
            message: The message to log.
            **kwargs: Additional context.

        """
        if self._structured:
            self._logger.info(message, **kwargs)
        else:
            self._logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message.

        Args:
            message: The message to log.
            **kwargs: Additional context.

        """
        if self._structured:
            self._logger.warning(message, **kwargs)
        else:
            self._logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message.

        Args:
            message: The message to log.
            **kwargs: Additional context.

        """
        if self._structured:
            self._logger.error(message, **kwargs)
        else:
            self._logger.error(self._format_message(message, **kwargs))

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message.

        Args:
            message: The message to log.
            **kwargs: Additional context.

        """
        if self._structured:
            self._logger.critical(message, **kwargs)
        else:
            self._logger.critical(self._format_message(message, **kwargs))

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log an exception with traceback.

        Args:
            message: The message to log.
            **kwargs: Additional context.

        """
        if self._structured:
            self._logger.exception(message, **kwargs)
        else:
            self._logger.exception(self._format_message(message, **kwargs))


def setup_logging(
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    *,
    format_type: Literal["simple", "detailed", "json"] = "detailed",
    log_file: str | None = None,
    use_structured: bool = False,
) -> None:
    """Configure the root logger.

    Args:
        level: Log level to set.
        format_type: Output format type.
        log_file: Optional file to log to.
        use_structured: Use structlog if available.

    """
    # Configure structlog if available and requested
    if use_structured and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                correlation_id_processor,
                mask_sensitive_data_processor,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
        )
        return

    # Standard logging configuration
    if format_type == "simple":
        log_format = "%(levelname)s: %(message)s"
    elif format_type == "json":
        log_format = JSON_FORMAT
    else:
        log_format = DEFAULT_FORMAT

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]

    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=handlers,
        force=True,
    )


def get_logger(
    name: str = "stack",
    *,
    level: str = "INFO",
    use_structured: bool = False,
) -> StackLogger:
    """Get a configured logger instance.

    Args:
        name: Logger name.
        level: Log level.
        use_structured: Use structlog if available.

    Returns:
        Configured StackLogger instance.

    Example:
        >>> logger = get_logger("my_module")
        >>> logger.bind(request_id="123").info("Processing request")

    """
    return StackLogger(name, level, use_structured=use_structured)


def log_operation(
    operation: str,
    *,
    logger: StackLogger | None = None,
    level: str = "INFO",
    expected_exceptions: tuple[type[Exception], ...] | type[Exception] = Exception,
) -> Any:
    """Context manager for logging operations.

    Args:
        operation: Name of the operation.
        logger: Logger to use (creates one if not provided).
        level: Log level for messages.
        expected_exceptions: Exceptions to catch and log as failures.

    Yields:
        The logger instance.

    Example:
        >>> with log_operation("setup") as logger:
        ...     logger.info("Setting up environment")

    """

    @contextmanager
    def _log_context() -> Any:
        nonlocal logger
        if logger is None:
            logger = get_logger()

        start_time = datetime.now(UTC)
        logger.bind(operation=operation)

        log_method = getattr(logger, level.lower())
        log_method(f"Starting: {operation}")

        try:
            yield logger
            duration = (datetime.now(UTC) - start_time).total_seconds()
            log_method(f"Completed: {operation}", duration_seconds=duration)
        except expected_exceptions as e:
            duration = (datetime.now(UTC) - start_time).total_seconds()
            logger.exception(
                f"Failed: {operation}",
                duration_seconds=duration,
                error=str(e),
            )
            raise
        finally:
            logger.unbind("operation")

    return _log_context()
