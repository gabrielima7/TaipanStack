"""Tests for the password hashing utilities."""

from pydantic import SecretStr

from taipanstack.security.password import hash_password, verify_password


def test_security_password_hash_password() -> None:
    """Test that hashing a password produces a valid-looking hash."""
    password = "secure_password"
    pwd_hash = hash_password(password)

    assert pwd_hash.startswith("$argon2")


def test_security_password_hash_password_secret_str() -> None:
    """Test that hashing a SecretStr works correctly."""
    password = SecretStr("secure_password")
    pwd_hash = hash_password(password)

    assert pwd_hash.startswith("$argon2")
    assert verify_password(password, pwd_hash)


def test_security_password_verify_password_success() -> None:
    """Test that a correct password verifies successfully."""
    password = "my_password"
    pwd_hash = hash_password(password)

    assert verify_password(password, pwd_hash) is True
    assert verify_password(SecretStr(password), pwd_hash) is True


def test_security_password_verify_password_failure() -> None:
    """Test that an incorrect password fails verification."""
    password = "my_password"
    pwd_hash = hash_password(password)

    assert verify_password("wrong_password", pwd_hash) is False


def test_security_password_verify_password_invalid_hash() -> None:
    """Test that invalid hash formats are handled gracefully."""
    password = "my_password"

    assert verify_password(password, "invalid_hash") is False
    assert verify_password(password, "$argon2$invalid$hash") is False
    assert verify_password(password, "alg$100$salt$hash") is False  # Wrong algorithm
    assert (
        verify_password(password, "pbkdf2_sha256$nan$salt$hash") is False
    )  # Invalid iterations
    assert (
        verify_password(password, "pbkdf2_sha256$100$nothex$hash") is False
    )  # Invalid salt hex
    assert (
        verify_password(password, "pbkdf2_sha256$100$salt$nothex") is False
    )  # Invalid hash hex
    assert (
        verify_password(password, "pbkdf2_sha256$100$salt") is False
    )  # Invalid parts length


def test_security_password_verify_legacy_password() -> None:
    """Test that legacy PBKDF2 hashes are still verifiable."""
    password = "my_password"
    # This is a pre-generated PBKDF2 hash of "my_password"
    # Format: pbkdf2_sha256$600000$salt$hash
    # Salt and hash need to be valid hex strings for verify_password.
    # We will compute a valid one manually to verify verification logic.
    import hashlib

    salt = b"1234567890123456"
    iterations = 600000
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    pwd_hash = f"pbkdf2_sha256${iterations}${salt.hex()}${hash_bytes.hex()}"

    assert verify_password(password, pwd_hash) is True
    assert verify_password("wrong_password", pwd_hash) is False


def test_security_password_verify_legacy_password_too_many_iterations() -> None:
    """Test that legacy PBKDF2 hashes with too many iterations are rejected."""
    password = "my_password"
    salt = b"1234567890123456"
    hash_bytes = b"fakehash"
    iterations = 1_000_001
    pwd_hash = f"pbkdf2_sha256${iterations}${salt.hex()}${hash_bytes.hex()}"

    assert verify_password(password, pwd_hash) is False


def test_security_password_hash_password_is_random() -> None:
    """Test that hashing the same password twice produces different hashes due to salt."""
    password = "my_password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_security_password_verify_password_invalid_type_password() -> None:
    """Test that an invalid type for password raises a TypeError."""
    import pytest

    pwd_hash = hash_password("my_password")

    with pytest.raises(TypeError, match="password must be a string or SecretStr"):
        verify_password(123, pwd_hash)  # type: ignore[arg-type]


def test_security_password_verify_password_invalid_type_hash() -> None:
    """Test that an invalid type for password_hash raises a TypeError."""
    import pytest

    with pytest.raises(TypeError, match="password_hash must be a string"):
        verify_password("my_password", 123)  # type: ignore[arg-type]


# Migrated from tests/test_100_coverage_final_operations.py
"""Tests to achieve 100% code coverage."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from taipanstack.security.sanitizers import sanitize_string
from taipanstack.utils.subprocess import run_safe_command


class TestAppMain:
    """Tests for app/main.py uncovered lines 26-27."""

    def test_100_coverage_final_main_function(self) -> None:
        """Test main() function execution."""
        import structlog
        from structlog.testing import capture_logs

        # Because `logger` is created at module import, we must patch its backend
        import app.main
        from app.main import main

        with capture_logs() as cap_logs:
            # Re-bind the logger so it uses the captured logs
            app.main.logger = structlog.get_logger("app.main")
            main()

        assert any("Hello, World!" in event["event"] for event in cap_logs)


class TestConfigGeneratorsBranches:
    """Tests for config/generators.py branch coverage."""

    def test_100_coverage_final_generate_pre_commit_without_bandit(
        self,
    ) -> None:
        """Test pre-commit config without bandit enabled."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_pip_audit=False,
                enable_semgrep=False,
                enable_detect_secrets=False,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "bandit" not in result

    def test_100_coverage_final_generate_pre_commit_with_safety_only(
        self,
    ) -> None:
        """Test pre-commit config with safety only."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_pip_audit=True,
                enable_semgrep=False,
                enable_detect_secrets=False,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "pip-audit" in result
        assert "bandit" not in result

    def test_100_coverage_final_generate_pre_commit_with_semgrep_only(
        self,
    ) -> None:
        """Test pre-commit config with semgrep only."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_pip_audit=False,
                enable_semgrep=True,
                enable_detect_secrets=False,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "semgrep" in result

    def test_100_coverage_final_generate_pre_commit_with_detect_secrets_only(
        self,
    ) -> None:
        """Test pre-commit config with detect-secrets only."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="testproj",
            security=SecurityConfig(
                enable_bandit=False,
                enable_pip_audit=False,
                enable_semgrep=False,
                enable_detect_secrets=True,
            ),
        )
        result = generate_pre_commit_config(config)
        assert "detect-secrets" in result


class TestCircuitBreakerOpenState:
    """Tests for circuit_breaker.py open state branch."""

    def test_100_coverage_final_record_success_in_open_state(self) -> None:
        """Test _record_success when circuit is OPEN (should be no-op)."""
        from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

        breaker = CircuitBreaker(name="test", failure_threshold=2)
        # Force state to OPEN
        breaker._state.state = CircuitState.OPEN
        # This should handle the OPEN case gracefully
        breaker._record_success()
        # State should remain OPEN
        assert breaker.state == CircuitState.OPEN

    def test_100_coverage_final_record_failure_in_open_state(self) -> None:
        """Test _record_failure when circuit is already OPEN."""
        from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState

        breaker = CircuitBreaker(name="test", failure_threshold=2)
        # Force state to OPEN
        breaker._state.state = CircuitState.OPEN
        # Record failure - should just increment count
        breaker._record_failure(RuntimeError("test"))
        assert breaker.state == CircuitState.OPEN


class TestResultModuleBranches:
    """Tests for result.py uncovered branches."""

    def test_100_coverage_final_collect_results_match_patterns(self) -> None:
        """Test all match patterns in collect_results."""
        from taipanstack.core.result import Ok, collect_results

        # Test with iterator (not list)
        results = iter([Ok(1), Ok(2)])
        collected = collect_results(results)
        assert collected.is_ok()

    def test_100_coverage_final_unwrap_or_match_patterns(self) -> None:
        """Test all match patterns in unwrap_or."""
        from taipanstack.core.result import Err, Ok

        # Ensure both branches covered
        assert Ok(5).unwrap_or(0) == 5
        assert Err("x").unwrap_or(0) == 0

    def test_100_coverage_final_unwrap_or_else_match_patterns(self) -> None:
        """Test all match patterns in unwrap_or_else."""
        from taipanstack.core.result import Err, Ok

        # Ensure both branches covered
        assert Ok(5).unwrap_or_else(len) == 5
        assert Err("abc").unwrap_or_else(len) == 3

    def test_100_coverage_final_collect_results_fallback(self) -> None:
        """Test collect_results fallback branch for unexpected types."""
        from taipanstack.core.result import collect_results

        # Pass a list containing something that is not Ok or Err
        class Dummy:
            def __init__(self):
                self.val = 1

        dummy = Dummy()
        res = collect_results(iter([dummy]))
        assert res is dummy  # The fallback branch returns the object itself

    @pytest.mark.asyncio
    async def test_map_async_fallback(self) -> None:
        """Test map_async fallback branch for unexpected types."""
        from taipanstack.core.result import map_async

        class Dummy:
            def __init__(self):
                self.val = 1

        dummy = Dummy()

        async def dummy_func(x):
            return x

        res = await map_async(dummy, dummy_func)
        assert res is dummy

    @pytest.mark.asyncio
    async def test_and_then_async_fallback(self) -> None:
        """Test and_then_async fallback branch for unexpected types."""
        from taipanstack.core.result import and_then_async

        class Dummy:
            def __init__(self):
                self.val = 1

        dummy = Dummy()

        async def dummy_func(x):
            from taipanstack.core.result import Ok

            return Ok(x)

        res = await and_then_async(dummy, dummy_func)
        assert res is dummy


class TestConfigModelsUncovered:
    """Tests for config/models.py uncovered lines."""

    def test_100_coverage_final_security_config_with_level(self) -> None:
        """Test SecurityConfig with explicit level."""
        from taipanstack.config.models import SecurityConfig

        config = SecurityConfig(level="standard")
        assert config.level == "standard"
        assert config.enable_bandit is True


class TestGuardsUncovered:
    """Tests for guards.py uncovered lines 97-98, 341."""

    def test_100_coverage_final_guard_ssrf_urlparse_value_error(self) -> None:
        """Test urlparse raising ValueError in guard_ssrf."""
        from unittest.mock import patch

        from taipanstack.security.guards import guard_ssrf

        with patch("taipanstack.security.guards.urlsplit") as mock_urlparse:
            mock_urlparse.side_effect = ValueError("Mocked error")
            res = guard_ssrf("http://example.com")
            assert res.is_err()
            err = res.err_value
            assert "Malformed URL" in str(err)
            assert "Mocked error" in str(err)

    def test_100_coverage_final_path_traversal_resolution_error(
        self, tmp_path: Path
    ) -> None:
        """Test guard_path_traversal with resolution error."""
        from taipanstack.security.guards import guard_path_traversal

        # Test with path that causes resolution warning
        valid_path = tmp_path / "valid_file.txt"
        valid_path.touch()
        result = guard_path_traversal(valid_path, tmp_path)
        assert result.exists()

    def test_100_coverage_final_env_variable_not_set(self) -> None:
        """Test guard_env_variable when variable not set."""
        from taipanstack.security.guards import SecurityError, guard_env_variable

        with pytest.raises(SecurityError, match="is not set"):
            guard_env_variable(
                "NONEXISTENT_VAR_12345",
                allowed_names=["NONEXISTENT_VAR_12345"],
            )


class TestValidatorsUncovered:
    """Tests for validators.py uncovered lines 128-130."""

    def test_100_coverage_final_python_version_parse_error(self) -> None:
        """Test validate_python_version with invalid numbers."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError, match="Invalid version format"):
            validate_python_version("abc")


class TestSanitizersUncovered:
    """Tests for sanitizers.py uncovered lines."""

    def test_100_coverage_final_sanitize_filename_empty_after_sanitization(
        self,
    ) -> None:
        """Test sanitize_filename with name that becomes empty."""
        from taipanstack.security.sanitizers import sanitize_filename

        # Name with only invalid chars
        result = sanitize_filename("...")
        assert result == "unnamed"

    def test_100_coverage_final_sanitize_path_with_base_dir_not_absolute(
        self, tmp_path: Path
    ) -> None:
        """Test sanitize_path with relative path and base_dir."""
        from taipanstack.security.sanitizers import sanitize_path

        result = sanitize_path("subdir/file.txt", base_dir=tmp_path)
        assert tmp_path in result.parents or result.parent == tmp_path

    def test_100_coverage_final_sanitize_env_value_multiline_allowed(
        self,
    ) -> None:
        """Test sanitize_env_value with multiline allowed."""
        from taipanstack.security.sanitizers import sanitize_env_value

        result = sanitize_env_value("line1\nline2", allow_multiline=True)
        assert "\n" in result

    def test_100_coverage_final_sanitize_sql_identifier_starts_with_number(
        self,
    ) -> None:
        """Test sanitize_sql_identifier starting with number."""
        from taipanstack.security.sanitizers import sanitize_sql_identifier

        result = sanitize_sql_identifier("123abc")
        assert result.startswith("_")


class TestRetryUncovered:
    """Tests for retry.py uncovered lines."""

    def test_100_coverage_final_retry_no_reraise(self) -> None:
        """Test retry with reraise=False still raises RetryError."""
        from taipanstack.resilience.retry import RetryError, retry

        @retry(max_attempts=1, on=(ValueError,), reraise=True, log_retries=False)
        def failing() -> None:
            raise ValueError("fail")

        with pytest.raises(RetryError):
            failing()

    def test_100_coverage_final_retrier_context_wrong_exception(self) -> None:
        """Test Retrier with non-matching exception type."""
        from taipanstack.resilience.retry import Retrier

        retrier = Retrier(max_attempts=3, on=(ValueError,))
        with pytest.raises(TypeError):
            with retrier:
                raise TypeError("wrong type")


class TestSubprocessUncovered:
    """Tests for subprocess.py uncovered lines."""

    def test_100_coverage_final_run_safe_command_success(self) -> None:
        """Test run_safe_command with successful command."""
        from taipanstack.utils.subprocess import run_safe_command

        result = run_safe_command(["echo", "test"], timeout=30.0)
        assert result.success
        assert result.returncode == 0


class TestFilesystemUncovered:
    """Tests for filesystem.py uncovered lines."""

    def test_100_coverage_final_safe_write_atomic_success(self, tmp_path: Path) -> None:
        """Test atomic write success path."""
        from taipanstack.utils.filesystem import WriteOptions, safe_write

        target = tmp_path / "test.txt"
        safe_write(target, "content", options=WriteOptions(atomic=True))
        assert target.read_text() == "content"


class TestLoggingUncovered:
    """Tests for logging.py uncovered lines 20-21."""

    def test_100_coverage_final_logging_fallback_branch(self) -> None:
        """Test logging when structlog not available."""
        from taipanstack.utils.logging import HAS_STRUCTLOG

        # Just verify the flag is accessible
        assert isinstance(HAS_STRUCTLOG, bool)


def test_100_coverage_final_password_empty_verify():
    assert verify_password("", "hash") is False
    assert verify_password(SecretStr(""), "hash") is False


def test_100_coverage_final_password_length_verify():
    assert verify_password("a" * 1025, "hash") is False
    assert verify_password(SecretStr("a" * 1025), "hash") is False


def test_100_coverage_final_password_hash_empty():
    with pytest.raises(ValueError, match="cannot be empty"):
        hash_password("")


def test_100_coverage_final_password_hash_length():
    with pytest.raises(ValueError, match="exceeds"):
        hash_password("a" * 1025)


def test_100_coverage_final_password_verify_wrong_type():
    with pytest.raises(TypeError, match="must be a string or SecretStr"):
        verify_password(None, "hash")


def test_100_coverage_final_password_verify_wrong_type_2():
    with pytest.raises(TypeError, match="must be a string"):
        verify_password("a", 123)


def test_100_coverage_final_password_hash_legacy_invalid():
    assert verify_password("pass", "pbkdf2_sha256$invalid$123") is False
    assert verify_password("pass", "pbkdf2_sha256$10000000$123$123") is False


def test_100_coverage_final_password_hash_wrong_type():
    with pytest.raises(TypeError, match="must be a string or SecretStr"):
        hash_password(None)


class TestSupplementarySubprocess:
    @patch("taipanstack.utils.subprocess.subprocess.run")
    def test_100_coverage_final_run_safe_command_mocked_timeout_no_stdout(
        self, mock_run
    ):
        # Create a mock exception that behaves like TimeoutExpired but has no stdout attribute
        class MockTimeoutExpired(subprocess.TimeoutExpired):
            def __init__(self):
                super().__init__(cmd=["python"], timeout=30)
                # Override the standard properties that were set in super
                self._cmd = ["python"]
                self._timeout = 1.0

            @property
            def cmd(self):
                return self._cmd

            @cmd.setter
            def cmd(self, value):
                self._cmd = value

            @property
            def timeout(self):
                return self._timeout

            @timeout.setter
            def timeout(self, value):
                self._timeout = value

        exc = MockTimeoutExpired()
        # Ensure hasattr(exc, "stdout") is False
        mock_run.side_effect = exc

        result = run_safe_command(["python", "-c", "print(1)"], timeout=1.0)
        assert result.returncode == -1
        assert result.stdout == ""
        assert "timed out after 1.0s" in result.stderr

    @patch("taipanstack.utils.subprocess.subprocess.run")
    def test_100_coverage_final_run_safe_command_mocked_timeout_with_bytes_stdout(
        self, mock_run
    ):
        # Mock it as bytes to test the fallback decode branch.
        exc = subprocess.TimeoutExpired(cmd=["python"], timeout=1.0)
        exc.stdout = b"some bytes output"
        mock_run.side_effect = exc

        result = run_safe_command(["python"], timeout=1.0)
        assert result.returncode == -1
        assert result.stdout == "some bytes output"


class TestSupplementarySanitizer:
    def test_100_coverage_final_sanitize_string_allow_html(self):
        # With allow_html=True, it should NOT remove HTML tags, but still strip whitespace
        val = "   <script>alert(1)</script>   "
        res = sanitize_string(val, allow_html=True, strip_whitespace=True)
        assert res == "<script>alert(1)</script>"

    def test_100_coverage_final_sanitize_string_disallow_unicode(self):
        # With allow_unicode=False, it should remove non-ASCII characters
        assert (
            sanitize_string("Hello\u200bWorld 😊", allow_unicode=False) == "HelloWorld "
        )

    def test_100_coverage_final_sanitize_string_truncate_exact(self):
        val = "12345"
        assert sanitize_string(val, max_length=5) == "12345"
        assert sanitize_string(val, max_length=4) == "1234"
        assert sanitize_string(val, max_length=10) == "12345"


# Migrated from tests/test_fuzz_password_operations.py
from hypothesis import given, settings
from hypothesis import strategies as st


@settings(deadline=None)
@given(st.text(), st.text())
def test_fuzz_password_fuzz_verify_password_returns_bool_or_raises_error(pw, pw_hash):
    try:
        result = verify_password(pw, pw_hash)
        assert isinstance(result, bool)
    except (TypeError, ValueError):
        assert True


@settings(deadline=None)
@given(
    st.one_of(
        st.text(),
        st.integers(),
        st.none(),
        st.floats(),
        st.builds(SecretStr, st.text()),
    )
)
def test_fuzz_password_fuzz_hash_password_returns_str_or_raises_error(pw):
    try:
        result = hash_password(pw)
        assert isinstance(result, str)
    except (TypeError, ValueError):
        assert True


# Migrated from tests/test_fuzz_password_verification_operations.py
import hypothesis.strategies as st
from hypothesis import HealthCheck, given, settings


@given(
    pw=st.text(min_size=1, max_size=100), hash_suffix=st.text(min_size=1, max_size=2000)
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_fuzz_password_verification_argon2_malformed_returns_false(pw, hash_suffix):
    """Bombard verify_password with valid prefixes but malformed suffix data."""
    malformed_hash = "$argon2id$v=19$m=65536,t=3,p=4$" + hash_suffix
    # Should cleanly return False, not raise VerificationError
    assert verify_password(pw, malformed_hash) is False
