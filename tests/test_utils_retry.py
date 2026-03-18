"""Tests for retry utilities."""

import pytest

from taipanstack.utils.retry import (
    Retrier,
    RetryConfig,
    RetryError,
    calculate_delay,
    retry,
    retry_on_exception,
)


class TestRetryConfig:
    """Tests for RetryConfig dataclass."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.initial_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = RetryConfig(
            max_attempts=5,
            initial_delay=0.5,
            max_delay=30.0,
        )
        assert config.max_attempts == 5
        assert config.initial_delay == 0.5
        assert config.max_delay == 30.0

    def test_frozen(self) -> None:
        """Test that config is immutable."""
        config = RetryConfig()
        with pytest.raises(AttributeError):
            config.max_attempts = 10


class TestCalculateDelay:
    """Tests for calculate_delay function."""

    def test_first_attempt_uses_initial_delay(self) -> None:
        """Test that first attempt uses initial delay."""
        config = RetryConfig(initial_delay=1.0, jitter=False)
        delay = calculate_delay(1, config)
        assert delay == 1.0

    def test_exponential_growth(self) -> None:
        """Test exponential backoff growth."""
        config = RetryConfig(
            initial_delay=1.0,
            exponential_base=2.0,
            jitter=False,
        )
        assert calculate_delay(1, config) == 1.0
        assert calculate_delay(2, config) == 2.0
        assert calculate_delay(3, config) == 4.0

    def test_max_delay_capped(self) -> None:
        """Test that delay is capped at max_delay."""
        config = RetryConfig(
            initial_delay=1.0,
            max_delay=5.0,
            jitter=False,
        )
        delay = calculate_delay(10, config)
        assert delay == 5.0

    def test_jitter_adds_randomness(self) -> None:
        """Test that jitter adds randomness."""
        config = RetryConfig(jitter=True, jitter_factor=0.5)

        delays = [calculate_delay(1, config) for _ in range(10)]
        # With 50% jitter, delays should vary
        assert len(set(delays)) > 1

    def test_chaos_retry_negative_attempt_resource_exhaustion(self) -> None:
        """Test resilience against negative attempt counter.

        Simulates a rare production failure/state mutation where `attempt` becomes
        negative, potentially causing a fractional exponential backoff result and
        resource exhaustion (near-zero micro-delay).
        """
        config = RetryConfig(initial_delay=1.0, exponential_base=2.0, jitter=False)

        # A negative attempt should be normalized to 1, returning the initial delay
        delay = calculate_delay(-5, config)

        assert delay == 1.0


class TestRetryDecorator:
    """Tests for @retry decorator."""

    def test_success_no_retry(self) -> None:
        """Test successful function doesn't retry."""
        call_count = 0

        @retry(max_attempts=3)
        def success_func() -> str:
            nonlocal call_count
            call_count += 1
            return "success"

        result = success_func()
        assert result == "success"
        assert call_count == 1

    def test_retry_on_failure(self) -> None:
        """Test function retries on failure."""
        call_count = 0

        @retry(max_attempts=3, initial_delay=0.01, on=(ValueError,))
        def failing_then_success() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"

        result = failing_then_success()
        assert result == "success"
        assert call_count == 3

    def test_max_attempts_exceeded(self) -> None:
        """Test RetryError when max attempts exceeded."""

        @retry(max_attempts=2, initial_delay=0.01, on=(ValueError,))
        def always_fail() -> None:
            raise ValueError("Always fails")

        with pytest.raises(RetryError) as exc_info:
            always_fail()
        assert exc_info.value.attempts == 2

    def test_only_catches_specified_exceptions(self) -> None:
        """Test that only specified exceptions trigger retry."""

        @retry(max_attempts=3, on=(ValueError,))
        def raise_type_error() -> None:
            raise TypeError("Wrong type")

        # TypeError should not be caught
        with pytest.raises(TypeError):
            raise_type_error()

    def test_last_exception_preserved(self) -> None:
        """Test that last exception is preserved in RetryError."""

        @retry(max_attempts=2, initial_delay=0.01, on=(ValueError,))
        def failing_func() -> None:
            raise ValueError("Original error")

        with pytest.raises(RetryError) as exc_info:
            failing_func()
        assert exc_info.value.last_exception is not None
        assert "Original error" in str(exc_info.value.last_exception)

    def test_on_retry_callback(self) -> None:
        """Test that on_retry callback is called."""
        retries = []

        def on_retry(
            attempt: int, max_attempts: int, exc: Exception, delay: float
        ) -> None:
            retries.append((attempt, max_attempts, exc, delay))

        @retry(max_attempts=3, initial_delay=0.01, on_retry=on_retry)
        def flaky() -> str:
            if len(retries) < 2:
                raise ValueError("fail")
            return "ok"

        result = flaky()
        assert result == "ok"
        assert len(retries) == 2
        assert retries[0][0] == 1
        assert retries[1][0] == 2

    def test_reraise_false(self) -> None:
        """Test reraise=False option."""

        @retry(max_attempts=2, initial_delay=0.01, reraise=False)
        def always_fail() -> None:
            raise ValueError("original")

        with pytest.raises(RetryError) as exc_info:
            always_fail()
        assert exc_info.value.__cause__ is None
        assert exc_info.value.last_exception is not None

    def test_max_attempts_zero(self) -> None:
        """Test max_attempts=0."""

        @retry(max_attempts=0)
        def never_runs() -> str:
            return "ok"

        with pytest.raises(RetryError) as exc_info:
            never_runs()
        assert exc_info.value.attempts == 0
        assert exc_info.value.last_exception is None


class TestAsyncRetryDecorator:
    """Tests for @retry decorator on async functions."""

    @pytest.mark.asyncio
    async def test_success_no_retry(self) -> None:
        """Test successful async function doesn't retry."""
        call_count = 0

        @retry(max_attempts=3)
        async def success_func() -> str:
            nonlocal call_count
            call_count += 1
            return "success"

        result = await success_func()
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_on_failure(self) -> None:
        """Test async function retries on failure."""
        call_count = 0

        @retry(max_attempts=3, initial_delay=0.01, on=(ValueError,))
        async def failing_then_success() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"

        result = await failing_then_success()
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_max_attempts_exceeded(self) -> None:
        """Test RetryError when max attempts exceeded for async function."""

        @retry(max_attempts=2, initial_delay=0.01, on=(ValueError,))
        async def always_fail() -> None:
            raise ValueError("Always fails")

        with pytest.raises(RetryError) as exc_info:
            await always_fail()
        assert exc_info.value.attempts == 2

    @pytest.mark.asyncio
    async def test_only_catches_specified_exceptions(self) -> None:
        """Test that only specified exceptions trigger retry for async function."""

        @retry(max_attempts=3, on=(ValueError,))
        async def raise_type_error() -> None:
            raise TypeError("Wrong type")

        # TypeError should not be caught
        with pytest.raises(TypeError):
            await raise_type_error()

    @pytest.mark.asyncio
    async def test_last_exception_preserved(self) -> None:
        """Test that last exception is preserved in RetryError for async function."""

        @retry(max_attempts=2, initial_delay=0.01, on=(ValueError,))
        async def failing_func() -> None:
            raise ValueError("Original error")

        with pytest.raises(RetryError) as exc_info:
            await failing_func()
        assert exc_info.value.last_exception is not None
        assert "Original error" in str(exc_info.value.last_exception)

    @pytest.mark.asyncio
    async def test_on_retry_callback(self) -> None:
        """Test that on_retry callback is called for async function."""
        retries = []

        def on_retry(
            attempt: int, max_attempts: int, exc: Exception, delay: float
        ) -> None:
            retries.append((attempt, max_attempts, exc, delay))

        @retry(max_attempts=3, initial_delay=0.01, on_retry=on_retry)
        async def flaky() -> str:
            if len(retries) < 2:
                raise ValueError("fail")
            return "ok"

        result = await flaky()
        assert result == "ok"
        assert len(retries) == 2
        assert retries[0][0] == 1
        assert retries[1][0] == 2

    @pytest.mark.asyncio
    async def test_reraise_false(self) -> None:
        """Test reraise=False option for async function."""

        @retry(max_attempts=2, initial_delay=0.01, reraise=False)
        async def always_fail() -> None:
            raise ValueError("original")

        with pytest.raises(RetryError) as exc_info:
            await always_fail()
        assert exc_info.value.__cause__ is None


class TestRetryOnException:
    """Tests for retry_on_exception decorator."""

    def test_simple_retry(self) -> None:
        """Test simple retry with retry_on_exception."""
        call_count = 0

        @retry_on_exception((ValueError,), max_attempts=2)
        def flaky_func() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("First fail")
            return "success"

        result = flaky_func()
        assert result == "success"
        assert call_count == 2

    def test_max_attempts_exceeded(self) -> None:
        """Test RetryError is raised when max attempts are exceeded."""
        call_count = 0

        @retry_on_exception((ValueError,), max_attempts=3)
        def always_fail() -> None:
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        with pytest.raises(RetryError) as exc_info:
            always_fail()

        assert exc_info.value.attempts == 3
        assert call_count == 3
        assert isinstance(exc_info.value.last_exception, ValueError)

    def test_other_exceptions_not_caught(self) -> None:
        """Test that unlisted exceptions are not caught and bubble up immediately."""
        call_count = 0

        @retry_on_exception((ValueError,), max_attempts=3)
        def raise_type_error() -> None:
            nonlocal call_count
            call_count += 1
            raise TypeError("Wrong type")

        with pytest.raises(TypeError):
            raise_type_error()

        assert call_count == 1


class TestRetrier:
    """Tests for Retrier context manager."""

    def test_successful_operation(self) -> None:
        """Test successful operation without retry."""
        retrier = Retrier(max_attempts=3)
        result = None

        with retrier:
            result = "success"

        assert result == "success"
        assert retrier.attempt == 0

    def test_tracks_attempts(self) -> None:
        """Test that retrier tracks attempt count."""
        # With max_attempts=1, exceção propaga na primeira tentativa
        retrier = Retrier(
            max_attempts=1,
            initial_delay=0.01,
            on=(ValueError,),
        )

        # Exception should propagate when max_attempts reached
        with pytest.raises(ValueError):
            with retrier:
                raise ValueError("fail")

        # Attempt was tracked
        assert retrier.attempt == 1

    def test_last_exception_stored(self) -> None:
        """Test that last exception is stored."""
        retrier = Retrier(max_attempts=1, on=(ValueError,))

        with pytest.raises(ValueError):
            with retrier:
                raise ValueError("stored error")

        assert retrier.last_exception is not None

    def test_retrier_unhandled_exception(self) -> None:
        """Test that Retrier doesn't catch unhandled exceptions."""
        retrier = Retrier(max_attempts=3, on=(ValueError,))

        with pytest.raises(TypeError):
            with retrier:
                raise TypeError("wrong")

        assert retrier.attempt == 0

    def test_retrier_suppression(self) -> None:
        """Test that Retrier suppresses exception and sleeps."""
        retrier = Retrier(max_attempts=3, initial_delay=0.01, on=(ValueError,))

        # First attempt - should be suppressed
        with retrier:
            raise ValueError("first")

        assert retrier.attempt == 1
        assert isinstance(retrier.last_exception, ValueError)

    def test_retrier_manual_loop(self) -> None:
        """Test Retrier in a manual retry loop."""
        retrier = Retrier(max_attempts=3, initial_delay=0.01, on=(ValueError,))
        attempts = 0

        while True:
            try:
                # Use 'with retrier' inside the loop to handle each attempt.
                # Note: __enter__ resets retrier.attempt to 0, but __exit__
                # will set it correctly for the current attempt if it fails.
                with retrier:
                    attempts += 1
                    if attempts < 3:
                        raise ValueError("fail")
                    break
            except ValueError:
                if attempts >= 3:
                    raise

        assert attempts == 3


class TestRetryError:
    """Tests for RetryError exception."""

    def test_has_attempts(self) -> None:
        """Test RetryError has attempts count."""
        error = RetryError("Failed", attempts=5)
        assert error.attempts == 5

    def test_has_last_exception(self) -> None:
        """Test RetryError has last exception."""
        original = ValueError("original")
        error = RetryError("Failed", attempts=3, last_exception=original)
        assert error.last_exception is original

    def test_message(self) -> None:
        """Test RetryError message."""
        error = RetryError("All attempts failed", attempts=3)
        assert "All attempts failed" in str(error)
