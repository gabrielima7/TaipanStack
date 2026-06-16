"""
Safe filesystem operations.

Provides secure wrappers around file operations with path validation,
atomic writes, and proper error handling using Result types.
"""

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

    @property
    def message(self) -> str:
        """Get the error message."""
        return f"File not found: {self.path}"


@dataclass(frozen=True)
class NotAFileErr:
    """Error when path is not a file."""

    path: Path

    @property
    def message(self) -> str:
        """Get the error message."""
        return f"Not a file: {self.path}"


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

    @property
    def message(self) -> str:
        """Get the error message."""
        return f"File too large: {self.size} bytes (max: {self.max_size})"


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


def _check_read_path(path: Path) -> Result[None, ReadFileError]:
    if not path.exists():
        return Err(FileNotFoundErr(path=path))
    if not path.is_file():
        return Err(NotAFileErr(path=path))
    return Ok(None)


def _check_read_size(
    path: Path,
    max_size_bytes: int | None,
) -> Result[None, ReadFileError]:
    if max_size_bytes is not None:
        file_size = path.stat().st_size
        if file_size > max_size_bytes:
            return Err(
                FileTooLargeErr(path=path, size=file_size, max_size=max_size_bytes),
            )
    return Ok(None)


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
        >>> result = safe_read("config.json")
        >>> if isinstance(result, Ok):
        ...     data = json.loads(result.unwrap())
        ... else:
        ...     err = result.unwrap_err()
        ...     if isinstance(err, FileNotFoundErr):
        ...         print(f"Missing: {err.path}")
        ...     elif isinstance(err, FileTooLargeErr):
        ...         print(f"Too big: {err.size} bytes")

    """
    path = Path(path)

    # Validate path
    try:
        path = _validate_path(path, base_dir)
    except SecurityError as e:
        return Err(e)

    path_check = _check_read_path(path)
    if isinstance(path_check, Err):
        return path_check

    size_check = _check_read_size(path, max_size_bytes)
    if isinstance(size_check, Err):
        return size_check

    return Ok(path.read_text(encoding=encoding))


def _validate_safe_write_path(path: Path, opts: WriteOptions) -> None:
    """Validate the path for safe_write."""
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


def _sanitize_write_path(path: Path) -> Path:
    """Sanitize the filename for safe_write."""
    safe_name = sanitize_filename(path.name)
    if safe_name != path.name:
        raise SecurityError(
            f"Unsafe or invalid characters in filename: '{path.name}'. "
            f"Expected safe name: '{safe_name}'",
            guard_name="sanitize_filename",
            value=path.name,
        )
    return path.parent / safe_name


def _perform_atomic_write(path: Path, content: str, opts: WriteOptions) -> None:
    """Perform an atomic write operation."""
    # Write to temp file first, then rename
    _fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    try:
        # Write directly to the returned file descriptor to prevent TOCTOU
        # We MUST close the file descriptor before renaming/modifying it,
        # otherwise Windows will throw a PermissionError (WinError 32).
        with os.fdopen(_fd, "w", encoding=opts.encoding) as f:
            f.write(content)
            f.flush()
            os.fsync(_fd)

        temp_file = Path(temp_path)
        # Preserve permissions if original exists
        if path.exists():
            shutil.copymode(path, temp_file)
        # On Windows, we need to remove the target first if it exists
        if path.exists():
            path.unlink()
        temp_file.rename(path)
    except BaseException:
        # Clean up temp file on error; _fd is already managed by the context manager's
        # __exit__ if the exception happens inside the block.
        # If it happens before/after, we unlink.
        Path(temp_path).unlink(missing_ok=True)
        raise


def _prepare_write_dir(path: Path, create_parents: bool) -> None:
    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)


def _create_write_backup(path: Path, backup: bool) -> None:
    if backup and path.exists():
        backup_path = path.with_suffix(f"{path.suffix}.bak")
        shutil.copy2(path, backup_path)


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

    _validate_safe_write_path(path, opts)
    path = _sanitize_write_path(path)

    _prepare_write_dir(path, opts.create_parents)
    _create_write_backup(path, opts.backup)

    # Write file
    if opts.atomic:
        _perform_atomic_write(path, content, opts)
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
        FileExistsError: If a file already exists at the given path or intermediate
            paths.

    """
    path = Path(path)

    # Validate path
    path = _validate_path(path, base_dir, allow_symlinks=True)
    resolved_path = path.resolve()

    # Identify missing parent directories from root to leaf
    paths_to_create: list[Path] = []
    current_path = resolved_path

    while not current_path.is_dir():
        if current_path.exists():
            raise FileExistsError(f"Path exists but is not a directory: {current_path}")
        paths_to_create.insert(0, current_path)
        parent = current_path.parent
        if parent == current_path:
            break
        current_path = parent

    # Iterate through parents and create them with specific mode
    for p in paths_to_create:
        p.mkdir(mode=mode, exist_ok=True)

    return resolved_path
