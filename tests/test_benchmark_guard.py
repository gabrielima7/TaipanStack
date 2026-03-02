import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from pathlib import Path

from taipanstack.security.guards import guard_file_extension, guard_env_variable
import os

def test_bench_guard_file_extension_allowed(benchmark: BenchmarkFixture) -> None:
    """Benchmark guard_file_extension with allowed extension."""
    benchmark(guard_file_extension, "safe_file.txt", allowed_extensions=["txt", "py", "md"])

def test_bench_guard_file_extension_denied(benchmark: BenchmarkFixture) -> None:
    """Benchmark guard_file_extension with denied extension."""
    def run_benchmark():
        try:
            guard_file_extension("unsafe_file.exe")
        except Exception:
            pass
    benchmark(run_benchmark)

def test_bench_guard_file_extension_custom_denied(benchmark: BenchmarkFixture) -> None:
    """Benchmark guard_file_extension with custom denied extensions."""
    def run_benchmark():
        try:
            guard_file_extension("custom_unsafe.bak", denied_extensions=["bak", "tmp", "old"])
        except Exception:
            pass
    benchmark(run_benchmark)

def test_bench_guard_env_variable_allowed(benchmark: BenchmarkFixture) -> None:
    """Benchmark guard_env_variable with allowed env variable."""
    os.environ["SAFE_TEST_VAR"] = "value"
    benchmark(guard_env_variable, "SAFE_TEST_VAR")

def test_bench_guard_env_variable_denied(benchmark: BenchmarkFixture) -> None:
    """Benchmark guard_env_variable with denied env variable."""
    def run_benchmark():
        try:
            guard_env_variable("AWS_SECRET_ACCESS_KEY")
        except Exception:
            pass
    benchmark(run_benchmark)

def test_bench_guard_env_variable_pattern_matched(benchmark: BenchmarkFixture) -> None:
    """Benchmark guard_env_variable with pattern-matched env variable."""
    def run_benchmark():
        try:
            guard_env_variable("MY_API_KEY")
        except Exception:
            pass
    benchmark(run_benchmark)
