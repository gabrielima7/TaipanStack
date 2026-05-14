# TaipanStack Standalone Executable Builder

This directory contains configuration for building standalone executables using [PyApp](https://ofek.dev/pyapp/).

## Prerequisites

- **Rust** toolchain installed (via [rustup](https://rustup.rs/))
- PyApp source code

## Quick Build

### Linux/macOS

```bash
./build.sh
```

### Windows

```powershell
.\build.ps1
```

## Manual Build

```bash
# Build the wheel first
poetry build

# Set PyApp configuration
export PYAPP_PROJECT_NAME="taipanstack-bootstrapper"
export PYAPP_PROJECT_VERSION="<YOUR_VERSION>"
export PYAPP_PYTHON_VERSION="3.11"
export PYAPP_PROJECT_PATH="dist/taipanstack-*.whl"
export PYAPP_EXEC_SCRIPT="taipanstack_bootstrapper.py"

# Build with cargo
cargo build --release

# Output: target/release/pyapp
```

## Configuration Options

See `pyapp.toml` for all configuration options.
