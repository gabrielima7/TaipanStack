#!/usr/bin/env python
"""
Automate the initial setup of a Python environment focused on
performance, security, and integrity.
"""

__version__ = "1.0.0"

import argparse
import platform
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

# Configuration Constants
PYPROJECT_TOML_PATH = Path("pyproject.toml")
PRE_COMMIT_CONFIG_PATH = Path(".pre-commit-config.yaml")
GITHUB_DIR = Path(".github")
DEPENDABOT_CONFIG_PATH = GITHUB_DIR / "dependabot.yml"
SECURITY_MD_PATH = Path("SECURITY.md")


# --- Utility Functions ---


def _log(message: str, args: argparse.Namespace, is_verbose: bool = False) -> None:
    """Centralized logging function that respects dry-run and verbose modes."""
    if is_verbose and not args.verbose:
        return
    print(message)


def _handle_error(message: str) -> NoReturn:
    """Display an error message and exit the script."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def _run_command(
    command: list[str], args: argparse.Namespace, capture_output: bool = False
) -> subprocess.CompletedProcess[str]:
    """Execute a shell command, handling errors and dry-run mode."""
    _log(f"Executing command: `{' '.join(command)}`", args, is_verbose=True)
    if args.dry_run:
        return subprocess.CompletedProcess(command, 0, "", "")

    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            encoding="utf-8",
            capture_output=capture_output,
        )
        return result
    except FileNotFoundError:
        # Poetry check is handled separately, so this is an unexpected error.
        _handle_error(
            f"Command '{command[0]}' not found. Make sure it is installed and in your PATH."
        )
    except subprocess.CalledProcessError as e:
        error_message = (
            f"Command `{' '.join(command)}` failed with exit code {e.returncode}."
        )
        if e.stderr and not capture_output:
            error_message += f"\nError:\n{e.stderr}"
        _handle_error(error_message)


def _is_windows() -> bool:
    """Check if the operating system is Windows."""
    return platform.system() == "Windows"


def _safe_write(path: Path, content: str, args: argparse.Namespace) -> None:
    """Write content to a file, with backup and dry-run mode support."""
    _log(f"Writing to file: {path}", args, is_verbose=True)
    if args.dry_run:
        return

    if path.exists() and not args.force:
        backup_path = path.with_suffix(f"{path.suffix}.bak")
        try:
            path.rename(backup_path)
            _log(f"⚠️  Backup created: {backup_path.name}", args)
        except (OSError, PermissionError) as e:
            _handle_error(f"Could not create backup for file {path.name}: {e}")

    try:
        path.write_text(content, encoding="utf-8")
    except (OSError, PermissionError) as e:
        _handle_error(f"Could not write to file {path.name}: {e}")


# --- Configuration Generation Functions ---


def _generate_pyproject_config(args: argparse.Namespace) -> None:
    """Generate and write Ruff and Mypy configurations to pyproject.toml."""
    _log(
        "📝 Generating configurations for Ruff, Mypy, and Pytest in pyproject.toml...",
        args,
    )

    try:
        pyproject_content = PYPROJECT_TOML_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        # If pyproject.toml doesn't exist, it means `poetry init` hasn't run yet.
        pyproject_content = ""

    config_to_add = ""

    if "[tool.ruff]" not in pyproject_content:
        python_version = f"py{sys.version_info.major}{sys.version_info.minor}"
        config_to_add += f"""
# --- Code Quality Configurations ---
[tool.ruff]
line-length = 88
target-version = "{python_version}"

[tool.ruff.lint]
select = [
    "F", "E", "W", "I", "N", "D", "Q", "S", "B", "A", "C4", "T20", "SIM", "PTH",
    "TID", "ARG", "PIE", "PLC", "PLE", "PLR", "PLW", "RUF"
]
ignore = ["D203", "D212", "D213", "D416", "D417", "B905"]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
"""

    if "[tool.mypy]" not in pyproject_content:
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        config_to_add += f"""
[tool.mypy]
python_version = "{python_version}"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = false
no_implicit_optional = true
check_untyped_defs = true
strict_optional = true
strict_equality = true
ignore_missing_imports = true
"""

    if "[tool.pytest.ini_options]" not in pyproject_content:
        config_to_add += """
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=80"
"""

    if not args.dry_run and config_to_add:
        try:
            with PYPROJECT_TOML_PATH.open("a", encoding="utf-8") as f:
                f.write(config_to_add)
        except (OSError, PermissionError) as e:
            _handle_error(f"Could not write to file pyproject.toml: {e}")
    elif args.dry_run and config_to_add:
        _log(
            "Would add tool configurations to pyproject.toml",
            args,
            is_verbose=True,
        )
    elif not config_to_add:
        _log(
            "✅ Configurations for Ruff, Mypy, and Pytest already exist in pyproject.toml.",
            args,
        )


def _generate_pre_commit_config(args: argparse.Namespace) -> None:
    """Generate and write the .pre-commit-config.yaml file."""
    _log("📝 Generating .pre-commit-config.yaml file...", args)
    config_content = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: 'v0.8.4'
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: 'v1.13.0'
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
  - repo: https://github.com/PyCQA/bandit
    rev: '1.8.0'
    hooks:
      - id: bandit
        args: ["-r", ".", "-ll"]
  - repo: https://github.com/pycqa/safety
    rev: '3.2.11'
    hooks:
      - id: safety
        args: ["scan", "--json"]
  - repo: https://github.com/semgrep/pre-commit
    rev: 'v1.99.0'
    hooks:
      - id: semgrep
        args: ['--config=auto']
  - repo: https://github.com/Yelp/detect-secrets
    rev: 'v1.5.0'
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
"""
    _safe_write(PRE_COMMIT_CONFIG_PATH, config_content, args)


def _generate_dependabot_config(args: argparse.Namespace) -> None:
    """Generate the Dependabot configuration file."""
    _log("📝 Generating .github/dependabot.yml file...", args)
    if not args.dry_run:
        try:
            GITHUB_DIR.mkdir(exist_ok=True)
        except (FileExistsError, PermissionError) as e:
            _handle_error(f"Could not create .github directory: {e}")
    config_content = """version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    groups:
      dev-dependencies:
        patterns:
          - "ruff"
          - "mypy"
          - "bandit"
          - "safety"
          - "pytest*"
          - "pre-commit"
          - "semgrep"
          - "py-spy"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
"""
    _safe_write(DEPENDABOT_CONFIG_PATH, config_content, args)


def _generate_security_policy(args: argparse.Namespace) -> None:
    """Generate the SECURITY.md file with a modern security policy."""
    _log("📝 Generating security policy in SECURITY.md...", args)
    content = """# Security Policy

## Supported Versions
We prioritize security patches in the latest version (Rolling Release).

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| Older   | :x:                |

## Reporting a Vulnerability
If you discover a vulnerability, please report it via the [Security](../../security) tab or by email.
"""
    _safe_write(SECURITY_MD_PATH, content, args)


# --- Orchestration Functions ---


def _check_git_initialized(args: argparse.Namespace) -> None:
    """Check if Git is initialized, and initialize it if necessary."""
    _log("🔎 Checking if Git is initialized...", args)
    git_dir = Path(".git")

    if git_dir.exists():
        _log("✅ Git repository already initialized.", args)
        return

    if not shutil.which("git"):
        _log("⚠️  Git not found in PATH. Skipping Git initialization.", args)
        return

    _log("🛠️  Initializing Git repository...", args)
    _run_command(["git", "init"], args)
    _log("✅ Git repository initialized successfully.", args)


def _check_connectivity(args: argparse.Namespace) -> None:
    """Check for internet connectivity before installing dependencies."""
    _log("🔎 Checking internet connectivity...", args, is_verbose=True)

    try:
        # Tries connecting to PyPI to verify connectivity
        socket.create_connection(("pypi.org", 443), timeout=5)
        _log("✅ Connectivity confirmed.", args, is_verbose=True)
    except (TimeoutError, OSError):
        _handle_error(
            "Could not connect to the internet. "
            "Please check your connection and proxies before proceeding."
        )


def _create_project_structure(args: argparse.Namespace) -> None:
    """Create the basic project folder structure."""
    _log("📁 Creating project folder structure...", args)

    # Detects the project name from pyproject.toml
    project_name = "my_project"
    if PYPROJECT_TOML_PATH.exists():
        try:
            content = PYPROJECT_TOML_PATH.read_text(encoding="utf-8")
            for line in content.split("\n"):
                if line.startswith("name = "):
                    project_name = line.split("=")[1].strip().strip('"').strip("'")
                    break
        except (OSError, IndexError):
            pass

    # Creates directory structure
    directories = [
        Path("src") / project_name,
        Path("tests"),
        Path("docs"),
    ]

    for directory in directories:
        if not args.dry_run:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                _log(f"✅ Created: {directory}", args, is_verbose=True)
            except (OSError, PermissionError) as e:
                _log(f"⚠️  Could not create {directory}: {e}", args)
        else:
            _log(f"Would create directory: {directory}", args, is_verbose=True)

    # Creates __init__.py files
    init_files = [
        Path("src") / project_name / "__init__.py",
        Path("tests") / "__init__.py",
    ]

    for init_file in init_files:
        if not init_file.exists() and not args.dry_run:
            try:
                content = f'"""Package initialization for {init_file.parent.name}."""\n'
                if init_file.parent.name == project_name:
                    content += '\n__version__ = "0.1.0"\n'
                init_file.write_text(content, encoding="utf-8")
                _log(f"✅ Created: {init_file}", args, is_verbose=True)
            except (OSError, PermissionError) as e:
                _log(f"⚠️  Could not create {init_file}: {e}", args)

    # Creates example main.py file
    main_file = Path("src") / project_name / "main.py"
    if not main_file.exists() and not args.dry_run:
        example_content = f'''"""Main module for {project_name}."""

def greet(name: str) -> str:
    """
    Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting message.
    """
    return f"Hello, {{name}}!"


def main() -> None:
    """Main entry point for the application."""
    message = greet("World")
    print(message)


if __name__ == "__main__":
    main()
'''
        try:
            main_file.write_text(example_content, encoding="utf-8")
            _log(f"✅ Created: {main_file}", args)
        except (OSError, PermissionError) as e:
            _log(f"⚠️  Could not create {main_file}: {e}", args)

    # Creates example test file
    test_file = Path("tests") / "test_example.py"
    if not test_file.exists() and not args.dry_run:
        test_content = f'''"""Example test module for {project_name}."""

from src.{project_name}.main import greet


def test_greet() -> None:
    """Test the greet function."""
    result = greet("Alice")
    assert result == "Hello, Alice!"
    assert isinstance(result, str)


def test_greet_empty() -> None:
    """Test greet with empty string."""
    result = greet("")
    assert result == "Hello, !"
'''
        try:
            test_file.write_text(test_content, encoding="utf-8")
            _log(f"✅ Created: {test_file}", args)
        except (OSError, PermissionError) as e:
            _log(f"⚠️  Could not create {test_file}: {e}", args)


def _validate_setup(args: argparse.Namespace) -> None:
    """Validate if the setup completed successfully."""
    _log("\n🔍 Validating setup...", args)

    issues = []

    # Checks required files
    required_files = [
        PYPROJECT_TOML_PATH,
        PRE_COMMIT_CONFIG_PATH,
        SECURITY_MD_PATH,
        DEPENDABOT_CONFIG_PATH,
    ]

    for file in required_files:
        if not file.exists():
            issues.append(f"File not found: {file}")

    # Checks if pre-commit is installed
    if shutil.which("poetry"):
        result = _run_command(
            ["poetry", "run", "pre-commit", "--version"], args, capture_output=True
        )
        if result.returncode != 0:
            issues.append("Pre-commit is not installed correctly")

    if issues:
        _log("⚠️  Issues found during validation:", args)
        for issue in issues:
            _log(f"  - {issue}", args)
    else:
        _log("✅ Validation completed successfully!", args)


def _check_poetry_installation(args: argparse.Namespace) -> None:
    """Check intelligently if Poetry is installed."""
    _log("🔎 Checking if Poetry is installed...", args)
    if shutil.which("poetry"):
        _log("✅ Poetry found.", args)
        return

    # If Poetry was not found, creates a more useful error message
    if shutil.which("pipx"):
        suggestion = "Try installing with: `pipx install poetry`"
    else:
        suggestion = "Consult the official documentation: https://python-poetry.org/docs/#installation"

    _handle_error(f"Poetry not found. {suggestion}")


def _initialize_poetry_project(args: argparse.Namespace) -> None:
    """Initialize a new Poetry project."""
    if PYPROJECT_TOML_PATH.exists():
        _log("✅ Poetry project already initialized.", args)
        return
    _log("🛠️  Initializing Poetry project...", args)
    _run_command(["poetry", "init", "-n"], args)


def _add_dependencies(args: argparse.Namespace) -> None:
    """Add production and development dependencies to the project."""
    # Production dependencies are optional
    if args.install_runtime_deps:
        _log("📦 Adding optional production dependencies...", args)
        prod_deps = ["pydantic>=2.0", "orjson"]
        if not _is_windows():
            prod_deps.append("uvloop")
        _run_command(["poetry", "add", *prod_deps], args)
    else:
        _log(
            "⏭️  Skipping production dependencies (use --install-runtime-deps to include them).",
            args,
        )

    _log("🔧 Adding development dependencies...", args)
    dev_deps = [
        "ruff",
        "mypy",
        "bandit",
        "safety",
        "pre-commit",
        "pytest",
        "pytest-cov",
        "py-spy",
        "semgrep",
    ]
    _run_command(["poetry", "add", "--group", "dev", *dev_deps], args)


def _setup_pre_commit_hooks(args: argparse.Namespace) -> None:
    """Install and configure pre-commit hooks."""
    _log("⚙️  Installing pre-commit hooks...", args)
    _run_command(["poetry", "run", "pre-commit", "install"], args)


def _setup_cli() -> argparse.Namespace:
    """Configure the command line interface."""
    parser = argparse.ArgumentParser(
        description="Automate the setup of a high-performance Python environment."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulates execution without making real changes to the file system.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Displays detailed logs about each step of the process.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Forces overwriting of configuration files without creating backups.",
    )
    parser.add_argument(
        "--install-runtime-deps",
        action="store_true",
        help="Installs optional production dependencies (pydantic, orjson, uvloop).",
    )
    return parser.parse_args()


def main() -> None:
    """Run the main entry point to orchestrate environment setup."""
    args = _setup_cli()

    _log(f"\n🐍 TaipanStack Bootstrapper v{__version__}", args)
    _log("Starting the setup of the high-performance Python environment...\n", args)

    # Initial checks
    _check_poetry_installation(args)
    _check_git_initialized(args)
    _check_connectivity(args)

    # Project initialization
    _initialize_poetry_project(args)
    _create_project_structure(args)

    # Dependency installation
    _add_dependencies(args)

    # Generation of configuration files
    _generate_pyproject_config(args)
    _generate_pre_commit_config(args)
    _generate_dependabot_config(args)
    _generate_security_policy(args)

    # Setup hooks
    _setup_pre_commit_hooks(args)

    # Final validation
    _validate_setup(args)

    # Final messages
    _log("\n✅ Environment setup successfully completed!", args)
    _log("Run `poetry shell` to activate the virtual environment.", args)
    _log(
        "💡 Tip: run `poetry config virtualenvs.in-project true` to create the .venv within the project.",
        args,
    )
    _log(
        "\n🔒 Remember to commit the `poetry.lock` file to guarantee reproducible builds.",
        args,
    )
    _log("\n📚 Consult the README.md for more information about the project.", args)


if __name__ == "__main__":
    main()
