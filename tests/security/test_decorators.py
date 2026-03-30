"""Tests for security decorators."""

import time
import warnings

import pytest

from taipanstack.security.decorators import (
    OperationTimeoutError,
    ValidationError,
    deprecated,
    guard_exceptions,
    require_type,
    timeout,
    validate_inputs,
)
from taipanstack.security.guards import SecurityError


class TestValidateInputs:
    """Tests for @validate_inputs decorator."""

    def test_valid_inputs_pass(self) -> None:
        """Test that valid inputs pass through."""

        def positive_int(x: int) -> int:
            if x <= 0:
                raise ValueError("Must be positive")
            return x

        @validate_inputs(n=positive_int)
        def double(n: int) -> int:
            return n * 2

        assert double(5) == 10

    def test_invalid_input_raises_validation_error(self) -> None:
        """Test that invalid input raises ValidationError."""

        def positive_int(x: int) -> int:
            if x <= 0:
                raise ValueError("Must be positive")
            return x

        @validate_inputs(n=positive_int)
        def double(n: int) -> int:
            return n * 2

        with pytest.raises(ValidationError, match="Must be positive"):
            double(-5)

    def test_validation_error_has_param_name(self) -> None:
        """Test that ValidationError includes parameter name."""

        def always_fail(x: str) -> None:
            raise ValueError("Always fails")

        @validate_inputs(name=always_fail)
        def greet(name: str) -> str:
            return f"Hello {name}"

        with pytest.raises(ValidationError) as exc_info:
            greet("test")
        assert exc_info.value.param_name == "name"

    def test_multiple_validators(self) -> None:
        """Test multiple validators on different params."""

        def min_length(s: str) -> str:
            if len(s) < 3:
                raise ValueError("Too short")
            return s

        def max_value(n: int) -> int:
            if n > 100:
                raise ValueError("Too large")
            return n

        @validate_inputs(name=min_length, age=max_value)
        def register(name: str, age: int) -> dict:
            return {"name": name, "age": age}

        # Valid
        result = register("Alice", 30)
        assert result["name"] == "Alice"

        # Invalid name
        with pytest.raises(ValidationError, match="Too short"):
            register("Al", 30)

        # Invalid age
        with pytest.raises(ValidationError, match="Too large"):
            register("Alice", 150)


class TestGuardExceptions:
    """Tests for @guard_exceptions decorator."""

    def test_no_exception_passes_through(self) -> None:
        """Test that successful execution passes through."""

        @guard_exceptions(catch=(ValueError,))
        def safe_func() -> str:
            return "success"

        assert safe_func() == "success"

    def test_caught_exception_returns_default(self) -> None:
        """Test that caught exception returns default."""

        @guard_exceptions(catch=(ValueError,), default="fallback")
        def failing_func() -> str:
            raise ValueError("error")

        assert failing_func() == "fallback"

    def test_uncaught_exception_propagates(self) -> None:
        """Test that uncaught exceptions propagate."""

        @guard_exceptions(catch=(ValueError,))
        def failing_func() -> str:
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            failing_func()

    def test_reraise_as_security_error(self) -> None:
        """Test reraising as SecurityError."""

        @guard_exceptions(catch=(IOError,), reraise_as=SecurityError)
        def read_file() -> str:
            raise OSError("file not found")

        with pytest.raises(SecurityError):
            read_file()

    def test_reraise_as_custom_exception(self) -> None:
        """Test reraising as custom exception type."""

        class CustomError(Exception):
            pass

        @guard_exceptions(catch=(ValueError,), reraise_as=CustomError)
        def failing_func() -> str:
            raise ValueError("original")

        with pytest.raises(CustomError):
            failing_func()


class TestTimeout:
    """Tests for @timeout decorator."""

    def test_fast_function_succeeds(self) -> None:
        """Test that fast functions succeed."""

        @timeout(5.0)
        def fast_func() -> str:
            return "done"

        assert fast_func() == "done"

    def test_slow_function_times_out(self) -> None:
        """Test that slow functions time out."""

        @timeout(0.1, use_signal=False)
        def slow_func() -> str:
            time.sleep(1)
            return "done"

        with pytest.raises(OperationTimeoutError):
            slow_func()

    def test_timeout_error_has_details(self) -> None:
        """Test OperationTimeoutError has seconds and func_name."""

        @timeout(0.1, use_signal=False)
        def named_func() -> None:
            time.sleep(1)

        with pytest.raises(OperationTimeoutError) as exc_info:
            named_func()
        assert exc_info.value.seconds == 0.1
        assert exc_info.value.func_name == "named_func"


class TestDeprecated:
    """Tests for @deprecated decorator."""

    def test_emits_deprecation_warning(self) -> None:
        """Test that deprecated function emits warning."""

        @deprecated("Use new_func instead")
        def old_func() -> str:
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_func()

        assert result == "old"
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "old_func is deprecated" in str(w[0].message)

    def test_includes_removal_version(self) -> None:
        """Test that removal version is included in warning."""

        @deprecated(removal_version="2.0")
        def old_func() -> None:
            pass

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            old_func()

        assert "version 2.0" in str(w[0].message)


class TestRequireType:
    """Tests for @require_type decorator."""

    def test_correct_types_pass(self) -> None:
        """Test that correct types pass through."""

        @require_type(name=str, count=int)
        def greet(name: str, count: int) -> str:
            return f"Hello {name}" * count

        assert greet("World", 2) == "Hello WorldHello World"

    def test_wrong_type_raises_type_error(self) -> None:
        """Test that wrong type raises TypeError."""

        @require_type(name=str)
        def greet(name: str) -> str:
            return f"Hello {name}"

        with pytest.raises(TypeError, match="expected str, got int"):
            greet(123)

    def test_multiple_type_checks(self) -> None:
        """Test checking multiple parameters."""

        @require_type(a=int, b=int)
        def add(a: int, b: int) -> int:
            return a + b

        assert add(1, 2) == 3

        with pytest.raises(TypeError):
            add("1", 2)


class TestDecoratorsEdgeCases:
    """Edge case tests for decorators module."""

    def test_timeout_with_signal(self) -> None:
        """Test timeout with signal (Unix only)."""
        import platform

        if platform.system() == "Windows":
            pytest.skip("Signal timeout not available on Windows")

        from taipanstack.security.decorators import OperationTimeoutError, timeout

        @timeout(0.1, use_signal=True)
        def slow_func() -> None:
            import time

            time.sleep(1)

        with pytest.raises(OperationTimeoutError):
            slow_func()


class TestDecoratorsComplete:
    """Complete tests for decorators module."""

    def test_validate_inputs_with_validation(self) -> None:
        """Test validate_inputs with actual validation."""
        from taipanstack.security.decorators import ValidationError, validate_inputs

        def must_be_positive(x: int) -> int:
            if x <= 0:
                raise ValueError("Must be positive")
            return x

        @validate_inputs(value=must_be_positive)
        def process(value: int) -> int:
            return value * 2

        # Valid input
        assert process(value=5) == 10

        # Invalid input
        with pytest.raises(ValidationError):
            process(value=-1)

    def test_guard_exceptions_reraise_non_security(self) -> None:
        """Test guard_exceptions with non-SecurityError reraise."""
        from taipanstack.security.decorators import guard_exceptions

        @guard_exceptions(catch=(ValueError,), reraise_as=TypeError)
        def raise_value_error() -> None:
            raise ValueError("original")

        with pytest.raises(TypeError):
            raise_value_error()

    def test_deprecated_with_removal_version(self) -> None:
        """Test deprecated with removal_version."""
        import warnings

        from taipanstack.security.decorators import deprecated

        @deprecated("Use new_func", removal_version="3.0.0")
        def old_func() -> str:
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_func()
            assert result == "old"
            assert len(w) == 1
            assert "3.0.0" in str(w[0].message)

    def test_require_type_passes(self) -> None:
        """Test require_type with valid types."""
        from taipanstack.security.decorators import require_type

        @require_type(name=str, count=int)
        def greet(name: str, count: int) -> str:
            return name * count

        result = greet(name="hi", count=2)
        assert result == "hihi"

    def test_require_type_fails(self) -> None:
        """Test require_type with invalid types."""
        from taipanstack.security.decorators import require_type

        @require_type(name=str)
        def greet(name: str) -> str:
            return name

        with pytest.raises(TypeError, match="expected str, got int"):
            greet(name=123)


class TestDecoratorsPartialBranches:
    """Test decorator partial branches."""

    def test_timeout_decorator_success(self) -> None:
        """Test timeout decorator when function completes in time."""
        from taipanstack.security.decorators import timeout

        @timeout(seconds=5)
        def quick_func() -> str:
            return "done"

        result = quick_func()
        assert result == "done"


class TestDecoratorsThreadTimeoutBranches:
    """Tests for thread timeout exception branches in decorators."""

    def test_timeout_thread_with_exception(self) -> None:
        """Test thread timeout when function raises exception."""
        from taipanstack.security.decorators import timeout

        @timeout(5.0, use_signal=False)
        def raise_error() -> None:
            raise ValueError("Expected error")

        with pytest.raises(ValueError, match="Expected error"):
            raise_error()

    def test_timeout_thread_success(self) -> None:
        """Test thread timeout with successful execution."""
        from taipanstack.security.decorators import timeout

        @timeout(5.0, use_signal=False)
        def success_func() -> str:
            return "success"

        result = success_func()
        assert result == "success"
