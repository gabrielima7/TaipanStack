"""
Safe filesystem operations.

Provides secure wrappers around file operations with path validation,
atomic writes, and proper error handling using Result types.
"""

import contextlib
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from taipanstack.core.result import Err, Ok, Result
from taipanstack.security.guards import (
    TRAVERSAL_REGEX,
    SecurityError,
    guard_path_traversal,
)
from taipanstack.security.sanitizers import sanitize_filename


@dataclass(frozen=True)
class FileNotFoundErr:
    """Error when file is not found."""

    path: Path
    message: str = ""

    def __post_init__(self) -> None:
        """Set default message."""
        object.__setattr__(
            self, "message", self.message or f"File not found: {self.path}"
        )


@dataclass(frozen=True)
class NotAFileErr:
    """Error when path is not a file."""

    path: Path
    message: str = ""

    def __post_init__(self) -> None:
        """Set default message."""
        object.__setattr__(self, "message", self.message or f"Not a file: {self.path}")


def _validate_path(
    path: Path | str,
    base_dir: Path | str | None = None,
    *,
    allow_symlinks: bool = False,
) -> Path:
    """Validate path for traversal.

    If base_dir is None, we only check for explicit traversal patterns
    to allow absolute paths (required for tests and some use cases),
    but still prevent '..' attacks.
    """
    path = Path(path)
    if base_dir is not None:
        return guard_path_traversal(path, base_dir, allow_symlinks=allow_symlinks)

    # Check for explicit traversal patterns
    path_str = str(path).lower()
    if TRAVERSAL_REGEX.search(path_str):
        raise SecurityError(
            "Path traversal pattern detected",
            guard_name="path_traversal",
            value=path_str[:50],
        )
    return path


@dataclass(frozen=True)
class FileTooLargeErr:
    """Error when file exceeds size limit."""

    path: Path
    size: int
    max_size: int
    message: str = ""

    def __post_init__(self) -> None:
        """Set default message."""
        object.__setattr__(
            self,
            "message",
            self.message or f"File too large: {self.size} bytes (max: {self.max_size})",
        )


@dataclass(frozen=True)
class WriteOptions:
    """Options for safe_write.

    Attributes:
        base_dir: Base directory to constrain to.
        encoding: File encoding.
        create_parents: Create parent directories if needed.
        backup: Create backup of existing file.
        atomic: Use atomic write.

    """

    base_dir: Path | str | None = None
    encoding: str = "utf-8"
    create_parents: bool = True
    backup: bool = True
    atomic: bool = True


# Union type for safe_read errors
ReadFileError: TypeAlias = (
    FileNotFoundErr | NotAFileErr | FileTooLargeErr | SecurityError
)


def safe_read(
    path: Path | str,
    *,
    base_dir: Path | str | None = None,
    encoding: str = "utf-8",
    max_size_bytes: int | None = 10 * 1024 * 1024,  # 10MB default
) -> Result[str, ReadFileError]:
    """Read a file safely with path validation.

    Args:
        path: Path to the file to read.
        base_dir: Base directory to constrain to.
        encoding: File encoding.
        max_size_bytes: Maximum file size to read (None for no limit).

    Returns:
        Ok(str): File contents on success.
        Err(ReadFileError): Error details on failure.

    Example:
        >>> match safe_read("config.json"):
        ...     case Ok(content):
        ...         data = json.loads(content)
        ...     case Err(FileNotFoundErr(path=p)):
        ...         print(f"Missing: {p}")
        ...     case Err(FileTooLargeErr(size=s)):
        ...         print(f"Too big: {s} bytes")

    """
    path = Path(path)

    # Validate path
    try:
        path = _validate_path(path, base_dir)
    except SecurityError as e:
        return Err(e)

    if not path.exists():
        return Err(FileNotFoundErr(path=path))

    if not path.is_file():
        return Err(NotAFileErr(path=path))

    # Check file size
    if max_size_bytes is not None:
        file_size = path.stat().st_size
        if file_size > max_size_bytes:
            return Err(
                FileTooLargeErr(path=path, size=file_size, max_size=max_size_bytes)
            )

    return Ok(path.read_text(encoding=encoding))


def safe_write(
    path: Path | str,
    content: str,
    *,
    options: WriteOptions | None = None,
) -> Path:
    """Write to a file safely with path validation.

    Args:
        path: Path to write to.
        content: Content to write.
        options: Write options.

    Returns:
        Path to the written file.

    Raises:
        SecurityError: If path validation fails.

    """
    opts = options or WriteOptions()
    path = Path(path)

    # Validate path
    if opts.base_dir is not None:
        base = Path(opts.base_dir).resolve()
        # For new files, validate the parent
        if not path.exists():
            parent = path.parent
            guard_path_traversal(parent, base)
        else:
            guard_path_traversal(path, base)
    else:
        _validate_path(path)

    # Sanitize filename
    safe_name = sanitize_filename(path.name)
    path = path.parent / safe_name

    # Create parents if needed
    if opts.create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)

    # Create backup if file exists
    if opts.backup and path.exists():
        backup_path = path.with_suffix(f"{path.suffix}.bak")
        shutil.copy2(path, backup_path)

    # Write file
    if opts.atomic:
        # Write to temp file first, then rename
        _fd, temp_path = tempfile.mkstemp(
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        )
        try:
            # Close the file descriptor immediately - required for Windows
            os.close(_fd)
            temp_file = Path(temp_path)
            temp_file.write_text(content, encoding=opts.encoding)
            # Preserve permissions if original exists
            if path.exists():
                shutil.copymode(path, temp_file)
            # On Windows, we need to remove the target first if it exists
            if path.exists():
                path.unlink()
            temp_file.rename(path)
        except Exception:
            # Clean up temp file on error
            with contextlib.suppress(OSError):
                Path(temp_path).unlink(missing_ok=True)
            raise
    else:
        path.write_text(content, encoding=opts.encoding)

    return path.resolve()


def ensure_dir(
    path: Path | str,
    *,
    base_dir: Path | str | None = None,
    mode: int = 0o755,
) -> Path:
    """Ensure a directory exists, creating it if needed.

    Args:
        path: Path to the directory.
        base_dir: Base directory to constrain to.
        mode: Directory permissions.

    Returns:
        Path to the directory.

    Raises:
        SecurityError: If path validation fails.

    """
    path = Path(path)

    # Validate path
    path = _validate_path(path, base_dir, allow_symlinks=True)

    path.mkdir(parents=True, exist_ok=True, mode=mode)
    return path.resolve()
