"""Performance benchmarks for TaipanStack critical-path functions.

Used by pytest-benchmark to detect performance regressions (>5%).
Run with: pytest tests/test_benchmarks.py --benchmark-only
"""

from __future__ import annotations

from result import Ok

from taipanstack.core.result import collect_results, safe, unwrap_or
from taipanstack.security.sanitizers import (
    sanitize_env_value,
    sanitize_filename,
    sanitize_path,
    sanitize_sql_identifier,
    sanitize_string,
)

# =============================================================================
# Sanitizer Benchmarks
# =============================================================================


def test_bench_sanitize_string_simple(benchmark) -> None:
    """Benchmark sanitize_string with typical input."""
    benchmark(sanitize_string, "Hello, World! This is a normal string.")


def test_bench_sanitize_string_xss(benchmark) -> None:
    """Benchmark sanitize_string with XSS payload."""
    benchmark(
        sanitize_string,
        "<script>alert('xss')</script><img onerror=alert(1) src=x>",
    )


def test_bench_sanitize_string_unicode(benchmark) -> None:
    """Benchmark sanitize_string with heavy unicode content."""
    benchmark(
        sanitize_string,
        "Héllo Wörld こんにちは 🌍 café résumé naïve" * 5,
    )


def test_bench_sanitize_filename_complex(benchmark) -> None:
    """Benchmark sanitize_filename with adversarial input."""
    benchmark(
        sanitize_filename,
        '../../../etc/passwd<>:"|?*CON.txt',
    )


def test_bench_sanitize_filename_long(benchmark) -> None:
    """Benchmark sanitize_filename with a very long name."""
    benchmark(sanitize_filename, "a" * 300 + ".txt", max_length=255)


def test_bench_sanitize_path_nested(benchmark) -> None:
    """Benchmark sanitize_path with nested directory structure."""
    benchmark(sanitize_path, "a/b/c/d/e/f/g/h/file.txt", max_depth=10)


def test_bench_sanitize_path_traversal(benchmark) -> None:
    """Benchmark sanitize_path with traversal attempts stripped."""
    benchmark(sanitize_path, "safe/../../still/../ok/file.txt", max_depth=None)


def test_bench_sanitize_env_value_standard(benchmark) -> None:
    """Benchmark sanitize_env_value with typical env content."""
    benchmark(
        sanitize_env_value,
        "DATABASE_URL=postgresql://user:pass@localhost:5432/db",
    )


def test_bench_sanitize_env_value_large(benchmark) -> None:
    """Benchmark sanitize_env_value with large payload."""
    benchmark(sanitize_env_value, "x" * 4096, max_length=4096)


def test_bench_sanitize_sql_identifier(benchmark) -> None:
    """Benchmark sanitize_sql_identifier with typical table name."""
    benchmark(sanitize_sql_identifier, "user_accounts_table")


def test_bench_sanitize_sql_identifier_dirty(benchmark) -> None:
    """Benchmark sanitize_sql_identifier with injection attempt."""
    benchmark(sanitize_sql_identifier, "users; DROP TABLE users--")


# =============================================================================
# Result Type Benchmarks
# =============================================================================


@safe
def _divide(a: int, b: int) -> float:
    """Test function for @safe decorator benchmarks."""
    return a / b


def test_bench_safe_decorator_ok(benchmark) -> None:
    """Benchmark @safe decorator on successful call."""
    benchmark(_divide, 10, 2)


def test_bench_safe_decorator_err(benchmark) -> None:
    """Benchmark @safe decorator on failing call."""
    benchmark(_divide, 10, 0)


def test_bench_collect_results_100(benchmark) -> None:
    """Benchmark collect_results with 100 Ok values."""
    results = [Ok(i) for i in range(100)]
    benchmark(collect_results, results)


def test_bench_unwrap_or(benchmark) -> None:
    """Benchmark unwrap_or with Ok value."""
    ok = Ok(42)
    benchmark(unwrap_or, ok, 0)
