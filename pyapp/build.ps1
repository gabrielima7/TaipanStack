# Build standalone executable using PyApp (Windows)
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Configuration
$env:PYAPP_PROJECT_NAME = "taipanstack-bootstrapper"
$env:PYAPP_PROJECT_VERSION = "0.5.0"
$env:PYAPP_PYTHON_VERSION = "3.11"
$env:PYAPP_EXEC_SCRIPT = Join-Path $ProjectRoot "taipanstack_bootstrapper.py"
$env:PYAPP_DISTRIBUTION_EMBED = "true"
$env:PYAPP_FULL_ISOLATION = "true"

# Build wheel first to ensure we have the latest code
Write-Host "Building wheel..."
Set-Location $ProjectRoot
poetry build
Set-Location $ScriptDir

# Find the built wheel
$env:PYAPP_PROJECT_PATH = Join-Path $ProjectRoot "dist\taipanstack-$($env:PYAPP_PROJECT_VERSION)-py3-none-any.whl"

if (-not (Test-Path $env:PYAPP_PROJECT_PATH)) {
    Write-Error "Error: Wheel file not found at $($env:PYAPP_PROJECT_PATH)"
    exit 1
}

# Check for Rust
if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Error "Error: Rust/Cargo is required. Install from https://rustup.rs/"
    exit 1
}

# Clone or update PyApp
$PyAppDir = Join-Path $ScriptDir ".pyapp-src"
if (Test-Path $PyAppDir) {
    Write-Host "Updating PyApp source..."
    git -C $PyAppDir pull --quiet
} else {
    Write-Host "Cloning PyApp source..."
    git clone --depth 1 https://github.com/ofek/pyapp.git $PyAppDir
}

# Build
Write-Host "Building standalone executable..."
Set-Location $PyAppDir
cargo build --release

# Copy output
$DistDir = Join-Path $ScriptDir "dist"
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null
Copy-Item (Join-Path $PyAppDir "target\release\pyapp.exe") (Join-Path $DistDir "taipanstack-bootstrapper.exe")

Write-Host ""
Write-Host "Build complete! Executable: $DistDir\taipanstack-bootstrapper.exe"
Write-Host ""
Write-Host "Usage:"
Write-Host "  .\dist\taipanstack-bootstrapper.exe --help"
Write-Host "  .\dist\taipanstack-bootstrapper.exe --dry-run"
