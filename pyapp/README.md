# Stack Standalone Executable Builder

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
# Set PyApp configuration
export PYAPP_PROJECT_NAME="stack-bootstrapper"
export PYAPP_PROJECT_VERSION="2.0.0"
export PYAPP_PYTHON_VERSION="3.11"
export PYAPP_EXEC_SCRIPT="stack_bootstrapper.py"

# Build with cargo
cargo build --release

# Output: target/release/stack-bootstrapper
```

## Configuration Options

See `pyapp.toml` for all configuration options.
