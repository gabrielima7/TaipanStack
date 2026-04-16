"""Tests for native structlog integration in retry.py and circuit_breaker.py."""

from unittest.mock import MagicMock, patch

import pytest


class TestRetryStructlogIntegration:
    """Test structlog auto-logging in the @retry decorator."""

    def test_retry_calls_structlog_warning_on_retry_without_callback_expected(
        self,
    ) -> None:
        """When no on_retry callback is provided, structlog.warning is called."""
        mock_structlog_logger = MagicMock()
        call_count = 0
        with (
            patch("taipanstack.resilience.retry._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.retry._structlog_logger", mock_structlog_logger
            ),
            patch("taipanstack.resilience.retry.time.sleep"),
        ):
            from taipanstack.resilience.retry import RetryError, retry

            @retry(max_attempts=2, initial_delay=0.0, jitter=False)
            def always_fails() -> int:
                nonlocal call_count
                call_count += 1
                msg = "boom"
                raise RuntimeError(msg)

            with pytest.raises(RetryError):
                always_fails()
        assert mock_structlog_logger.warning.call_count >= 1
        call_kwargs = mock_structlog_logger.warning.call_args
        assert call_kwargs is not None
        assert call_kwargs[0][0] == "retry_attempted"

    def test_retry_does_not_call_structlog_when_callback_provided_expected(
        self,
    ) -> None:
        """When on_retry callback is provided, structlog should NOT be called."""
        mock_structlog_logger = MagicMock()
        callback_calls: list[tuple[int, int, Exception, float]] = []
        with (
            patch("taipanstack.resilience.retry._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.retry._structlog_logger", mock_structlog_logger
            ),
            patch("taipanstack.resilience.retry.time.sleep"),
        ):
            from taipanstack.resilience.retry import retry

            @retry(
                max_attempts=2,
                initial_delay=0.0,
                jitter=False,
                on_retry=lambda a, m, e, d: callback_calls.append((a, m, e, d)),
            )
            def fails_once() -> int:
                if len(callback_calls) == 0:
                    msg = "first fail"
                    raise ValueError(msg)
                return 42

            assert fails_once() == 42
        mock_structlog_logger.warning.assert_not_called()

    def test_retry_structlog_warning_has_expected_fields_expected(self) -> None:
        """Verify that structlog.warning receives all expected kwargs."""
        mock_structlog_logger = MagicMock()
        with (
            patch("taipanstack.resilience.retry._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.retry._structlog_logger", mock_structlog_logger
            ),
            patch("taipanstack.resilience.retry.time.sleep"),
        ):
            from taipanstack.resilience.retry import RetryError, retry

            @retry(max_attempts=2, initial_delay=0.0, jitter=False)
            def named_failing_fn() -> None:
                msg = "err"
                raise OSError(msg)

            with pytest.raises(RetryError):
                named_failing_fn()
        warning_calls = mock_structlog_logger.warning.call_args_list
        assert warning_calls, "Expected at least one structlog.warning call"
        _, kwargs = warning_calls[0]
        assert "function" in kwargs
        assert "attempt" in kwargs
        assert "max_attempts" in kwargs
        assert "error" in kwargs
        assert "delay_seconds" in kwargs
        assert kwargs["function"] == "named_failing_fn"

    def test_retry_no_structlog_no_crash_expected(self) -> None:
        """When _HAS_STRUCTLOG is False, retries must still work silently."""
        with (
            patch("taipanstack.resilience.retry._HAS_STRUCTLOG", False),
            patch("taipanstack.resilience.retry._structlog_logger", None),
            patch("taipanstack.resilience.retry.time.sleep"),
        ):
            from taipanstack.resilience.retry import retry

            attempt_counter = {"n": 0}

            @retry(max_attempts=2, initial_delay=0.0, jitter=False)
            def recovers_on_second() -> str:
                attempt_counter["n"] += 1
                if attempt_counter["n"] < 2:
                    msg = "transient"
                    raise ConnectionError(msg)
                return "ok"

            result = recovers_on_second()
            assert result == "ok"


class TestCircuitBreakerStructlogIntegration:
    """Test structlog auto-logging in CircuitBreaker state transitions."""

    def test_circuit_breaker_calls_structlog_on_state_change_without_callback_expected(
        self,
    ) -> None:
        """Without on_state_change, structlog.warning is emitted on circuit open."""
        mock_structlog_logger = MagicMock()
        with (
            patch("taipanstack.resilience.circuit_breaker._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.circuit_breaker._structlog_logger",
                mock_structlog_logger,
            ),
        ):
            from taipanstack.resilience.circuit_breaker import CircuitBreaker

            breaker = CircuitBreaker(failure_threshold=1, name="test_circuit")

            @breaker
            def always_fails() -> None:
                msg = "fail"
                raise RuntimeError(msg)

            with pytest.raises(RuntimeError):
                always_fails()
        assert mock_structlog_logger.warning.call_count >= 1
        call_args = mock_structlog_logger.warning.call_args
        assert call_args is not None
        assert call_args[0][0] == "circuit_state_changed"

    def test_circuit_breaker_structlog_fields_are_correct_expected(self) -> None:
        """Verify structlog.warning kwargs contain expected circuit fields."""
        mock_structlog_logger = MagicMock()
        with (
            patch("taipanstack.resilience.circuit_breaker._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.circuit_breaker._structlog_logger",
                mock_structlog_logger,
            ),
        ):
            from taipanstack.resilience.circuit_breaker import CircuitBreaker

            breaker = CircuitBreaker(failure_threshold=1, name="field_check_circuit")

            @breaker
            def fail_fn() -> None:
                msg = "x"
                raise RuntimeError(msg)

            with pytest.raises(RuntimeError):
                fail_fn()
        warning_calls = mock_structlog_logger.warning.call_args_list
        assert warning_calls
        _, kwargs = warning_calls[0]
        assert "circuit" in kwargs
        assert "old_state" in kwargs
        assert "new_state" in kwargs
        assert "failure_count" in kwargs
        assert kwargs["circuit"] == "field_check_circuit"

    def test_circuit_breaker_does_not_call_structlog_when_callback_provided_expected(
        self,
    ) -> None:
        """When on_state_change callback is set, structlog must NOT be called."""
        mock_structlog_logger = MagicMock()
        transitions: list[tuple[object, object]] = []
        with (
            patch("taipanstack.resilience.circuit_breaker._HAS_STRUCTLOG", True),
            patch(
                "taipanstack.resilience.circuit_breaker._structlog_logger",
                mock_structlog_logger,
            ),
        ):
            from taipanstack.resilience.circuit_breaker import CircuitBreaker

            breaker = CircuitBreaker(
                failure_threshold=1,
                name="callback_circuit",
                on_state_change=lambda o, n: transitions.append((o, n)),
            )

            @breaker
            def fail_again() -> None:
                msg = "err"
                raise RuntimeError(msg)

            with pytest.raises(RuntimeError):
                fail_again()
        mock_structlog_logger.warning.assert_not_called()
        assert len(transitions) >= 1

    def test_circuit_breaker_no_structlog_no_crash_expected(self) -> None:
        """Without structlog, circuit breaker must operate normally."""
        with (
            patch("taipanstack.resilience.circuit_breaker._HAS_STRUCTLOG", False),
            patch("taipanstack.resilience.circuit_breaker._structlog_logger", None),
        ):
            from taipanstack.resilience.circuit_breaker import CircuitBreaker

            breaker = CircuitBreaker(failure_threshold=1, name="no_structlog")

            @breaker
            def fn() -> None:
                msg = "fail"
                raise RuntimeError(msg)

            with pytest.raises(RuntimeError):
                fn()
            from taipanstack.resilience.circuit_breaker import CircuitState

            assert breaker.state == CircuitState.OPEN
