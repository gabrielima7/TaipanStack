#!/usr/bin/env python3
"""
TaipanStack Version Bump Utility.
Enforces the custom rollover rule:
- Patch version increments up to 10 (e.g. 0.6.9 -> 0.6.10).
- At patch 10, rolls over to minor increment and resets patch to 0 (e.g. 0.6.10 -> 0.7.0).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION_PATTERN = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def calculate_next_version(current_version: str) -> str:
    """Calculate the next version string based on .10 rollover rule.

    Args:
        current_version: String version like '0.7.0' or 'v0.6.10'.

    Returns:
        New version string without 'v' prefix, e.g. '0.7.1' or '0.7.0'.

    Raises:
        ValueError: If current_version does not conform to x.y.z.
    """
    clean_version = current_version.strip()
    match = VERSION_PATTERN.match(clean_version)
    if not match:
        raise ValueError(
            f"Invalid version format: '{current_version}'. Expected format: [v]MAJOR.MINOR.PATCH"
        )

    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))

    if patch < 10:
        new_patch = patch + 1
        return f"{major}.{minor}.{new_patch}"
    else:
        new_minor = minor + 1
        return f"{major}.{new_minor}.0"


def get_current_project_version(root_dir: Path | None = None) -> str:
    """Read version directly from pyproject.toml."""
    if root_dir is None:
        root_dir = Path(__file__).resolve().parent.parent

    pyproject_file = root_dir / "pyproject.toml"
    if not pyproject_file.exists():
        raise FileNotFoundError(f"pyproject.toml not found in {root_dir}")

    content = pyproject_file.read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find 'version' field in pyproject.toml")
    return match.group(1)


def update_project_files(new_version: str, root_dir: Path | None = None, dry_run: bool = False) -> None:
    """Update version in pyproject.toml and src/taipanstack/__init__.py."""
    if root_dir is None:
        root_dir = Path(__file__).resolve().parent.parent

    pyproject_file = root_dir / "pyproject.toml"
    init_file = root_dir / "src" / "taipanstack" / "__init__.py"

    # 1. Update pyproject.toml
    pyproject_content = pyproject_file.read_text(encoding="utf-8")
    new_pyproject_content = re.sub(
        r'(?m)^version\s*=\s*["\'][^"\']+["\']',
        f'version = "{new_version}"',
        pyproject_content,
        count=1,
    )

    # 2. Update __init__.py
    init_content = init_file.read_text(encoding="utf-8")
    new_init_content = re.sub(
        r'(?m)^__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        init_content,
        count=1,
    )

    if dry_run:
        print(f"[DRY RUN] Would update {pyproject_file} and {init_file} to version {new_version}")
        return

    pyproject_file.write_text(new_pyproject_content, encoding="utf-8")
    init_file.write_text(new_init_content, encoding="utf-8")
    print(f"Updated {pyproject_file} and {init_file} to version {new_version}")


def main() -> None:
    parser = argparse.ArgumentParser(description="TaipanStack version bump tool with .10 rollover rule.")
    parser.add_argument(
        "--current",
        type=str,
        default=None,
        help="Specify current version explicitly instead of reading pyproject.toml",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Calculate and show next version without writing files",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write new version into pyproject.toml and __init__.py",
    )
    args = parser.parse_args()

    current_ver = args.current or get_current_project_version()
    next_ver = calculate_next_version(current_ver)

    if args.apply:
        update_project_files(next_ver, dry_run=args.dry_run)
    else:
        print(next_ver)


if __name__ == "__main__":
    main()
