"""
Configuration watcher — detects file changes and hot-reloads config.

Polls configuration files for modifications using SHA-256 hashes
and validates new content via Pydantic before applying changes.
"""

import hashlib
import json
import logging
from collections.abc import Callable, Sequence
from pathlib import Path

from pydantic import BaseModel, ValidationError

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.watchdogs._base import BaseWatcher

logger = logging.getLogger("taipanstack.resilience.watchdogs.config")

MAX_CONFIG_FILE_SIZE = 1048576


def _hash_file(path: Path) -> Result[str, Exception]:
    """Compute the SHA-256 hex digest of a file.

    Args:
        path: Path to the file.

    Returns:
        ``Ok(hex_digest)`` on success, ``Err`` on I/O failure.

    """
    try:
        if path.stat().st_size > MAX_CONFIG_FILE_SIZE:
            return Err(
                ValueError(
                    f"File {path} exceeds max size ({MAX_CONFIG_FILE_SIZE} bytes)"
                )
            )
        data = path.read_bytes()
        return Ok(hashlib.sha256(data).hexdigest())
    except OSError as exc:
        return Err(exc)


def _parse_env(text: str) -> dict[str, object]:
    """Parse a simple ``.env`` key=value file.

    Lines starting with ``#`` or blank lines are skipped.
    Surrounding quotes on values are stripped.

    Args:
        text: Raw text content of the ``.env`` file.

    Returns:
        Parsed key-value mapping.

    """
    result: dict[str, object] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        value = value.strip().strip("\"'")
        result[key.strip()] = value
    return result


def _parse_json(text: str) -> Result[dict[str, object], Exception]:
    """Parse JSON text.

    Args:
        text: Raw JSON string.

    Returns:
        ``Ok(dict)`` on success, ``Err`` on parse failure.

    """
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            return Err(TypeError(f"Expected JSON object, got {type(data).__name__}"))
        return Ok(data)
    except (json.JSONDecodeError, ValueError) as exc:
        return Err(exc)


def _read_file_content(path: Path) -> Result[str, Exception]:
    """Read file content with size validation."""
    try:
        if path.stat().st_size > MAX_CONFIG_FILE_SIZE:
            return Err(
                ValueError(
                    f"File {path} exceeds max size ({MAX_CONFIG_FILE_SIZE} bytes)"
                )
            )
        return Ok(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return Err(exc)


def _parse_content_by_extension(
    path: Path, text: str
) -> Result[dict[str, object], Exception]:
    """Parse file content based on extension."""
    suffix = path.suffix.lower()
    if suffix == ".json":
        return _parse_json(text)
    if suffix == ".env" or path.name == ".env":
        return Ok(_parse_env(text))

    return Err(ValueError(f"Unsupported config file extension: {suffix}"))


def _load_file_data(path: Path) -> Result[dict[str, object], Exception]:
    """Read and parse a configuration file based on its extension.

    Supported extensions: ``.env``, ``.json``.

    Args:
        path: Path to the config file.

    Returns:
        ``Ok(dict)`` with parsed data, or ``Err`` on failure.

    """
    content_result = _read_file_content(path)
    if isinstance(content_result, Err):
        return content_result

    return _parse_content_by_extension(path, content_result.ok_value)


def validate_config(
    data: dict[str, object],
    model: type[BaseModel],
) -> Result[BaseModel, Exception]:
    """Validate a data dictionary against a Pydantic model.

    Args:
        data: Raw configuration data.
        model: Pydantic model class to validate against.

    Returns:
        ``Ok(model_instance)`` on success, ``Err(ValidationError)``
        on failure.

    """
    try:
        return Ok(model.model_validate(data))
    except ValidationError as exc:
        return Err(exc)


class ConfigWatcher(BaseWatcher):
    """Background watcher that detects configuration file changes.

    Polls file hashes at each interval. When a change is detected
    the content is validated via the provided Pydantic model and,
    if valid, the ``on_config_change`` callback is invoked.

    Args:
        config_paths: Files to watch.
        config_model: Pydantic model for validation.
        interval: Seconds between polls.
        on_config_change: Callback receiving the validated model.
        on_validation_error: Callback receiving the ``Exception``
            when validation fails.

    Example:
        >>> watcher = ConfigWatcher(
        ...     config_paths=[Path(".env")],
        ...     config_model=MySettings,
        ...     on_config_change=lambda cfg: apply(cfg),
        ... )
        >>> await watcher.start()

    """

    def __init__(
        self,
        *,
        config_paths: Sequence[Path],
        config_model: type[BaseModel],
        interval: float = 2.0,
        on_config_change: Callable[[BaseModel], None] | None = None,
        on_validation_error: Callable[[Exception], None] | None = None,
    ) -> None:
        """Initialize the config watcher.

        Args:
            config_paths: Files to watch.
            config_model: Pydantic model for validation.
            interval: Seconds between polls.
            on_config_change: Callback for valid config changes.
            on_validation_error: Callback for validation failures.

        """
        super().__init__(interval=interval)
        self._config_paths = list(config_paths)
        self._config_model = config_model
        self._on_config_change = on_config_change
        self._on_validation_error = on_validation_error
        self._file_hashes: dict[Path, str] = {}

    def _process_hash_result(
        self, path: Path, current_hash: str, changed: list[Path]
    ) -> None:
        """Process successful hash result and update changed list."""
        previous = self._file_hashes.get(path)
        if previous is None:
            # First time seeing this file — record hash
            self._file_hashes[path] = current_hash
        elif current_hash != previous:
            self._file_hashes[path] = current_hash
            changed.append(path)

    def _detect_changes(self) -> Result[list[Path], Exception]:
        """Detect which watched files have changed since last check.

        Returns:
            ``Ok(list[Path])`` of changed file paths.

        """
        changed: list[Path] = []
        for path in self._config_paths:
            hash_result = _hash_file(path)
            if isinstance(hash_result, Ok):
                self._process_hash_result(path, hash_result.ok_value, changed)
            else:
                logger.warning("Cannot hash %s: %s", path, hash_result.err_value)
        return Ok(changed)

    def _handle_validation_success(
        self, path: Path, model: BaseModel
    ) -> Result[BaseModel, Exception]:
        """Handle successful validation."""
        logger.info(
            "Config hot-reloaded from %s",
            path,
        )
        if self._on_config_change is not None:
            self._on_config_change(model)
        return Ok(model)

    def _handle_validation_failure(
        self, path: Path, val_error: Exception
    ) -> Result[BaseModel, Exception]:
        """Handle validation failure."""
        logger.error(
            "Config validation failed for %s: %s",
            path,
            val_error,
        )
        if self._on_validation_error is not None:
            self._on_validation_error(val_error)
        return Err(val_error)

    def _validate_and_apply(self, path: Path) -> Result[BaseModel, Exception]:
        """Load, validate, and apply configuration from a file.

        Args:
            path: Path to the changed config file.

        Returns:
            ``Ok(model)`` if valid, ``Err`` otherwise.

        """
        load_result = _load_file_data(path)
        if isinstance(load_result, Err):
            return Err(load_result.err_value)
        validation = validate_config(load_result.ok_value, self._config_model)
        if isinstance(validation, Ok):
            return self._handle_validation_success(path, validation.ok_value)
        return self._handle_validation_failure(path, validation.err_value)

    async def _run(self) -> None:
        """Execute a single config-check cycle."""
        changes = self._detect_changes()
        if isinstance(changes, Ok):
            for path in changes.ok_value:
                self._validate_and_apply(path)
        else:
            logger.error("Change detection failed: %s", changes.err_value)
