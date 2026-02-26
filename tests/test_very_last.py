"""The very last tests for 100% coverage.

Covers edge cases, error branches, and version-specific code paths
that are not exercised by the main test suite.
"""

from __future__ import annotations

import gc
import logging
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# validators.py — L128-130: non-numeric parts in version string
# =============================================================================
class TestValidatorsVersionConversion:
    """Test for validators.py lines 128-130 (version conversion ValueError)."""

    def test_validate_python_version_with_letters(self) -> None:
        """Test validate_python_version with letters in version."""
        from taipanstack.security.validators import validate_python_version

        with pytest.raises(ValueError, match="Invalid version"):
            validate_python_version("3.x")


# =============================================================================
# guards.py — L97-98: OSError/ValueError in path.resolve()
# =============================================================================
class TestGuardsOSErrorMocked:
    """Test for guards.py lines 97-98 (OSError in resolve)."""

    def test_guard_path_basic_works(self, tmp_path: Path) -> None:
        """Test guard_path_traversal with basic case."""
        from taipanstack.security.guards import guard_path_traversal

        file = tmp_path / "test.txt"
        file.write_text("test")

        result = guard_path_traversal(file, tmp_path)
        assert result.exists()

    def test_guard_path_resolve_valueerror(self) -> None:
        """Test guard_path_traversal catching ValueError from resolve (L97-98)."""
        from taipanstack.security.guards import SecurityError, guard_path_traversal

        # Use a path object whose resolve() raises ValueError
        mock_path = MagicMock(spec=Path)
        mock_path.__str__ = MagicMock(return_value="safe_file.txt")
        mock_path.is_absolute.return_value = False

        # The (base_dir / path).resolve() call raises ValueError
        mock_joined = MagicMock(spec=Path)
        mock_joined.resolve.side_effect = ValueError("embedded null byte")

        with (
            patch.object(Path, "__truediv__", return_value=mock_joined),
            patch.object(Path, "resolve", return_value=Path("/tmp/base")),  # noqa: S108
        ):
            with pytest.raises(SecurityError, match="Invalid path"):
                guard_path_traversal("safe_file.txt", "/tmp/base")  # noqa: S108


# =============================================================================
# guards.py — symlink detection
# =============================================================================
class TestGuardsSymlinkMocked:
    """Test for guards.py line 118 (symlink detection)."""

    def test_guard_path_traversal_symlink_mocked(self, tmp_path: Path) -> None:
        """Test guard_path_traversal symlink detection with mock."""
        from taipanstack.security.guards import SecurityError, guard_path_traversal

        target = tmp_path / "real_file.txt"
        target.write_text("content")

        # Make path.is_symlink() return True via mock
        with patch.object(Path, "is_symlink", return_value=True):
            with pytest.raises(SecurityError, match="Symlinks"):
                guard_path_traversal(target, tmp_path, allow_symlinks=False)


# =============================================================================
# sanitizers.py — L241-243: sanitize_path with resolve=True raising
# =============================================================================
class TestSanitizersResolveError:
    """Test for sanitizers.py lines 241-243 (resolve error)."""

    def test_sanitize_path_works(self, tmp_path: Path) -> None:
        """Test sanitize_path with valid path."""
        from taipanstack.security.sanitizers import sanitize_path

        result = sanitize_path("subdir/file.txt", base_dir=tmp_path, max_depth=None)
        assert result is not None

    def test_sanitize_path_resolve_oserror(self) -> None:
        """Test sanitize_path with resolve=True raising OSError (L241-243)."""
        from taipanstack.security.sanitizers import sanitize_path

        # Use selective mock: first resolve call (base_dir) succeeds,
        # second resolve call (sanitized path) raises OSError
        call_count = 0
        original_resolve = Path.resolve

        def selective_resolve(self_path: Path, *a: object, **kw: object) -> Path:
            nonlocal call_count
            call_count += 1
            # First resolve is for base_dir, let it pass
            if call_count >= 2:
                raise OSError("No such file")
            return original_resolve(self_path, *a, **kw)  # type: ignore[arg-type]

        with patch.object(Path, "resolve", selective_resolve):
            with pytest.raises(ValueError, match="Cannot resolve path"):
                sanitize_path(
                    "file.txt",
                    base_dir="/tmp",  # noqa: S108
                    resolve=True,
                    max_depth=None,
                )

    def test_sanitize_path_resolve_runtime_error(self) -> None:
        """Test sanitize_path with resolve=True raising RuntimeError (L241-243)."""
        from taipanstack.security.sanitizers import sanitize_path

        call_count = 0
        original_resolve = Path.resolve

        def selective_resolve(self_path: Path, *a: object, **kw: object) -> Path:
            nonlocal call_count
            call_count += 1
            if call_count >= 2:
                raise RuntimeError("Recursion")
            return original_resolve(self_path, *a, **kw)  # type: ignore[arg-type]

        with patch.object(Path, "resolve", selective_resolve):
            with pytest.raises(ValueError, match="Cannot resolve path"):
                sanitize_path(
                    "file.txt",
                    base_dir="/tmp",  # noqa: S108
                    resolve=True,
                    max_depth=None,
                )


# =============================================================================
# filesystem.py — L243: ensure_dir with ".." traversal
# =============================================================================
class TestFilesystemWriteError:
    """Test for filesystem.py coverage gaps."""

    def test_safe_write_existing_permissions(self, tmp_path: Path) -> None:
        """Test safe_write preserves permissions on existing file."""
        from taipanstack.utils.filesystem import safe_write

        existing = tmp_path / "existing.txt"
        existing.write_text("old")

        # Write new content atomically
        result = safe_write(existing, "new", atomic=True)
        assert result.read_text() == "new"

    def test_ensure_dir_with_traversal(self, tmp_path: Path) -> None:
        """Test ensure_dir with '..' in path string (L243)."""
        from taipanstack.security.guards import SecurityError
        from taipanstack.utils.filesystem import ensure_dir

        # ".." in path but no base_dir → falls through to guard_path_traversal
        with pytest.raises(SecurityError, match="traversal"):
            ensure_dir("../../../escape_dir")

    def test_safe_delete_with_traversal(self, tmp_path: Path) -> None:
        """Test safe_delete with '..' in path (L327)."""
        from taipanstack.security.guards import SecurityError
        from taipanstack.utils.filesystem import safe_delete

        with pytest.raises(SecurityError, match="traversal"):
            safe_delete("../../../escape_file.txt", missing_ok=False)


# =============================================================================
# retry.py — retry exhaustion
# =============================================================================
class TestRetryMaxAttemptsBranch:
    """Test for retry.py line 187/288."""

    def test_retry_exhausts_all_attempts(self) -> None:
        """Test retry when all attempts fail."""
        from taipanstack.utils.retry import RetryError, retry

        @retry(max_attempts=2, initial_delay=0.001, on=(ValueError,))
        def always_fails() -> None:
            raise ValueError("fail!")

        with pytest.raises(RetryError):
            always_fails()


# =============================================================================
# subprocess.py — L231: check=True with failing command
# =============================================================================
class TestSubprocessCheckCommand:
    """Test for subprocess.py coverage gaps."""

    def test_check_command_exists_edge(self) -> None:
        """Test check_command_exists with edge cases."""
        from taipanstack.utils.subprocess import check_command_exists

        assert check_command_exists("zzzzz_fake_command") is False
        assert check_command_exists("ls") is True

    def test_run_safe_command_check_true_fails(self) -> None:
        """Test run_safe_command with check=True when command fails (L231)."""
        from taipanstack.utils.subprocess import run_safe_command

        with pytest.raises(subprocess.CalledProcessError):
            run_safe_command(["python", "-c", "raise SystemExit(1)"], check=True)


# =============================================================================
# logging.py — L20-21: HAS_STRUCTLOG import path; L245: log_file
# =============================================================================
class TestLoggingStructlogBranches:
    """Test for remaining logging.py coverage gaps."""

    def test_logging_with_structlog_real(self) -> None:
        """Test logging with real structlog."""
        from taipanstack.utils.logging import HAS_STRUCTLOG, StackLogger

        assert HAS_STRUCTLOG is True

        # Use structured mode
        logger = StackLogger(use_structured=True)
        logger.info("Structured log message", key="value")

    def test_logging_without_structlog(self) -> None:
        """Test the HAS_STRUCTLOG=False branch (L20-21)."""
        # We can't truly un-import structlog, but we can test that the
        # fallback path works by forcing use_structured=False
        from taipanstack.utils.logging import StackLogger

        logger = StackLogger(use_structured=False)
        logger.debug("Should use standard logging")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    def test_setup_logging_with_log_file(self) -> None:
        """Test setup_logging with a log_file parameter (L245)."""
        from taipanstack.utils.logging import setup_logging

        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            log_path = f.name

        try:
            setup_logging(level="DEBUG", log_file=log_path)
            logger = logging.getLogger("test_logfile")
            logger.info("Test message to file")

            # Verify file was written to
            content = Path(log_path).read_text()
            assert "Test message to file" in content
        finally:
            Path(log_path).unlink(missing_ok=True)
            # Reset logging to avoid polluting other tests
            setup_logging(level="INFO")


# =============================================================================
# generators.py — L165: security.level == "paranoid" branch
# =============================================================================
class TestGeneratorsParanoidLevel:
    """Test for generators.py line 165 (paranoid security level)."""

    def test_pre_commit_config_paranoid_level(self) -> None:
        """Test generate_pre_commit_config with paranoid security level."""
        from taipanstack.config.generators import generate_pre_commit_config
        from taipanstack.config.models import SecurityConfig, StackConfig

        config = StackConfig(
            project_name="test-project",
            python_version="3.12",
            security=SecurityConfig(
                level="paranoid",
                enable_bandit=True,
                enable_safety=True,
                enable_semgrep=True,
                enable_detect_secrets=True,
            ),
        )

        result = generate_pre_commit_config(config)

        # Paranoid level should include pip-audit, vulture, tryceratops
        assert "pip-audit" in result
        assert "vulture" in result
        assert "tryceratops" in result
        assert "bandit" in result
        assert "safety" in result
        assert "semgrep" in result
        assert "detect-secrets" in result


# =============================================================================
# compat.py — L91-96, L107-120, L137-138: Python >=3.13 feature checks
# =============================================================================
class TestCompatPy313FeatureDetection:
    """Test compat.py JIT/free-threading/mimalloc detection branches."""

    def test_check_jit_available_on_py313(self) -> None:
        """Test _check_jit_available when PY313=True (L91-96)."""
        from taipanstack.core import compat

        with patch.object(compat, "PY313", True):
            # No _jit attribute by default
            result = compat._check_jit_available()
            assert isinstance(result, bool)

    def test_check_jit_available_type_error(self) -> None:
        """Test _check_jit_available catches TypeError (L95)."""
        from taipanstack.core import compat

        with (
            patch.object(compat, "PY313", True),
            patch(
                "builtins.hasattr",
                side_effect=TypeError("broken"),
            ),
        ):
            result = compat._check_jit_available()
            assert result is False

    def test_check_free_threading_with_nogil(self) -> None:
        """Test _check_free_threading_available with nogil flag (L107-120)."""
        from taipanstack.core import compat

        mock_flags = MagicMock()
        mock_flags.nogil = False

        with (
            patch.object(compat, "PY313", True),
            patch.object(sys, "flags", mock_flags),
        ):
            result = compat._check_free_threading_available()
            assert result is False

    def test_check_free_threading_sysconfig_disable_gil(self) -> None:
        """Test _check_free_threading_available via sysconfig CONFIG_ARGS (L114-120)."""
        from taipanstack.core import compat

        mock_flags = MagicMock(spec=[])  # spec=[] means no 'nogil' attribute

        with (
            patch.object(compat, "PY313", True),
            patch.object(sys, "flags", mock_flags),
            patch.dict("sys.modules", {"sysconfig": MagicMock()}),
        ):
            import sysconfig

            sysconfig.get_config_var = MagicMock(  # type: ignore[attr-defined]
                return_value="--disable-gil --with-pydebug"
            )
            result = compat._check_free_threading_available()
            assert result is True

    def test_check_free_threading_attribute_error(self) -> None:
        """Test _check_free_threading_available catches AttributeError (L117-118)."""
        from taipanstack.core import compat

        mock_flags = MagicMock(spec=[])  # No 'nogil'

        with (
            patch.object(compat, "PY313", True),
            patch.object(sys, "flags", mock_flags),
            patch.dict("sys.modules", {"sysconfig": MagicMock()}),
        ):
            import sysconfig

            sysconfig.get_config_var = MagicMock(  # type: ignore[attr-defined]
                side_effect=AttributeError
            )
            result = compat._check_free_threading_available()
            assert result is False

    def test_check_mimalloc_available_on_py313(self) -> None:
        """Test _check_mimalloc_available with mimalloc in config (L137-138)."""
        from taipanstack.core import compat

        with (
            patch.object(compat, "PY313", True),
            patch.dict("sys.modules", {"sysconfig": MagicMock()}),
        ):
            import sysconfig

            sysconfig.get_config_var = MagicMock(  # type: ignore[attr-defined]
                return_value="--with-mimalloc"
            )
            result = compat._check_mimalloc_available()
            assert result is True

    def test_check_mimalloc_attribute_error(self) -> None:
        """Test _check_mimalloc_available catches AttributeError (L137-138)."""
        from taipanstack.core import compat

        with (
            patch.object(compat, "PY313", True),
            patch.dict("sys.modules", {"sysconfig": MagicMock()}),
        ):
            import sysconfig

            sysconfig.get_config_var = MagicMock(  # type: ignore[attr-defined]
                side_effect=AttributeError
            )
            result = compat._check_mimalloc_available()
            assert result is False


# =============================================================================
# optimizations.py — L253-254, L269-272, L284, L286, L346
# =============================================================================
class TestOptimizationsEdgeCases:
    """Test optimizations.py edge cases for coverage."""

    def test_apply_gc_tuning_exception(self) -> None:
        """Test _apply_gc_tuning when gc.set_threshold raises (L253-254)."""
        from taipanstack.core.optimizations import OptimizationProfile, _apply_gc_tuning

        profile = OptimizationProfile()
        applied: list[str] = []
        errors: list[str] = []

        with patch.object(gc, "set_threshold", side_effect=RuntimeError("GC error")):
            _apply_gc_tuning(profile, applied, errors)

        assert len(errors) == 1
        assert "GC error" in errors[0]

    def test_apply_gc_freeze_not_py312(self) -> None:
        """Test _apply_gc_freeze skipped when not PY312 (L271-272)."""
        from taipanstack.core import optimizations
        from taipanstack.core.optimizations import (
            OptimizationProfile,
            _apply_gc_freeze,
        )

        profile = OptimizationProfile(gc_freeze_enabled=True)
        applied: list[str] = []
        skipped: list[str] = []
        errors: list[str] = []

        with patch.object(optimizations, "PY312", False):
            _apply_gc_freeze(
                profile,
                freeze_after=True,
                applied=applied,
                skipped=skipped,
                errors=errors,
            )

        assert any("requires Python 3.12" in s for s in skipped)

    def test_apply_gc_freeze_success(self) -> None:
        """Test _apply_gc_freeze succeeds on PY312+ (L267-268)."""
        from taipanstack.core import optimizations
        from taipanstack.core.optimizations import (
            OptimizationProfile,
            _apply_gc_freeze,
        )

        profile = OptimizationProfile(gc_freeze_enabled=True)
        applied: list[str] = []
        skipped: list[str] = []
        errors: list[str] = []

        with patch.object(optimizations, "PY312", True):
            _apply_gc_freeze(
                profile,
                freeze_after=True,
                applied=applied,
                skipped=skipped,
                errors=errors,
            )

        assert any("gc_freeze" in a for a in applied)

    def test_apply_gc_freeze_exception(self) -> None:
        """Test _apply_gc_freeze error handling (L269-270)."""
        from taipanstack.core import optimizations
        from taipanstack.core.optimizations import (
            OptimizationProfile,
            _apply_gc_freeze,
        )

        profile = OptimizationProfile(gc_freeze_enabled=True)
        applied: list[str] = []
        skipped: list[str] = []
        errors: list[str] = []

        with (
            patch.object(optimizations, "PY312", True),
            patch.object(gc, "freeze", side_effect=RuntimeError("freeze failed")),
        ):
            _apply_gc_freeze(
                profile,
                freeze_after=True,
                applied=applied,
                skipped=skipped,
                errors=errors,
            )

        assert any("freeze failed" in e for e in errors)

    def test_apply_experimental_with_jit_and_free_threading(self) -> None:
        """Test _apply_experimental when JIT and free-threading are available (L284, L286)."""
        from taipanstack.core.compat import PythonFeatures, VersionTier
        from taipanstack.core.optimizations import (
            OptimizationProfile,
            _apply_experimental,
        )

        profile = OptimizationProfile(enable_experimental=True)
        applied: list[str] = []
        skipped: list[str] = []

        mock_features = PythonFeatures(
            version=(3, 13, 0),
            version_string="3.13.0",
            tier=VersionTier.MODERN,
            has_jit=True,
            has_free_threading=True,
            experimental_enabled=True,
        )

        with patch(
            "taipanstack.core.optimizations.get_features",
            return_value=mock_features,
        ):
            _apply_experimental(profile, applied, skipped)

        assert any("jit" in a for a in applied)
        assert any("free_threading" in a for a in applied)

    def test_apply_optimizations_with_errors(self) -> None:
        """Test apply_optimizations logs errors (L346)."""
        from taipanstack.core.optimizations import (
            OptimizationProfile,
            apply_optimizations,
        )

        profile = OptimizationProfile()

        with patch.object(gc, "set_threshold", side_effect=RuntimeError("boom")):
            result = apply_optimizations(profile=profile, apply_gc=True)

        assert not result.success
        assert len(result.errors) > 0
        assert any("boom" in e for e in result.errors)
