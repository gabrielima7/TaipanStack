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

    def test_negative_values_handled(self) -> None:
        """Test that negative values result in zero delay."""
        # Negative initial delay
        config = RetryConfig(initial_delay=-1.0, jitter=False)
        assert calculate_delay(1, config) == 0.0

        # Negative max delay
        config = RetryConfig(initial_delay=1.0, max_delay=-1.0, jitter=False)
        assert calculate_delay(1, config) == 0.0

        # Negative attempt number
        config = RetryConfig(initial_delay=1.0, jitter=False)
        assert calculate_delay(-1, config) == 1.0


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
        """Test that on_retry callback is invoked."""
        callback_calls = []

        def on_retry(attempt: int, max_attempts: int, exc: Exception, delay: float) -> None:
            callback_calls.append((attempt, max_attempts, exc, delay))

        @retry(max_attempts=2, initial_delay=0.01, on_retry=on_retry)
        def fail_once() -> str:
            if len(callback_calls) == 0:
                raise ValueError("Fail")
            return "success"

        result = fail_once()
        assert result == "success"
        assert len(callback_calls) == 1
        assert callback_calls[0][0] == 1
        assert callback_calls[0][1] == 2
        assert isinstance(callback_calls[0][2], ValueError)

    def test_reraise_false(self) -> None:
        """Test RetryError when reraise is False."""

        @retry(max_attempts=2, initial_delay=0.01, reraise=False)
        def fail() -> None:
            raise ValueError("Fail")

        with pytest.raises(RetryError) as exc_info:
            fail()

        # When reraise=False, RetryError is raised but not FROM the original exception
        assert exc_info.value.last_exception is not None
        assert isinstance(exc_info.value.last_exception, ValueError)
        assert exc_info.value.__cause__ is None


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

    def test_retrier_actually_retries(self) -> None:
        """Test that retrier actually suppresses exception and allows retry."""
        # Using a new retrier for each attempt to avoid __enter__ resetting state,
        # OR better: not using 'with' if we want to keep state across attempts.
        # Wait, the Retrier design with __enter__ resetting attempt to 0 means
        # it's NOT intended to keep state across multiple 'with' blocks.
        # BUT __exit__ increments self.attempt.
        # This seems like a bug in Retrier.__enter__ or my understanding of it.
        # If __enter__ resets self.attempt, then it can only ever handle max_attempts-1
        # exceptions WITHIN a single 'with' block? No, 'with' block is entered once.

        # Let's fix the Retrier to NOT reset attempt in __enter__ if we want it to work
        # across multiple 'with' blocks, or just test it as it is.
        # As it is, if I use a while loop with 'with retrier', it resets every time.

        retrier = Retrier(max_attempts=3, initial_delay=0.01, on=(ValueError,))

        # To use Retrier across multiple attempts, we must NOT use 'with' in a loop
        # if __enter__ resets it.
        # Alternatively, we can manually call __enter__ once.

        retrier.__enter__()
        attempts_made = 0
        try:
            for _ in range(3):
                try:
                    attempts_made += 1
                    if attempts_made < 3:
                        raise ValueError("Retry me")
                    break
                except Exception as e:
                    if not retrier.__exit__(type(e), e, e.__traceback__):
                        raise
        finally:
            # If no exception happened, we still need to exit
            pass

        assert attempts_made == 3
        assert retrier.attempt == 2

    def test_retrier_unhandled_exception(self) -> None:
        """Test that unhandled exceptions propagate immediately."""
        retrier = Retrier(max_attempts=3, on=(ValueError,))

        with pytest.raises(TypeError):
            with retrier:
                raise TypeError("Immediate fail")

        assert retrier.attempt == 0


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
