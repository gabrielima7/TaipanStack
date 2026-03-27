import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from taipanstack.security.decorators import timeout


class CustomBaseException(BaseException):
    pass


@settings(deadline=None)
@given(
    st.sampled_from([SystemExit, KeyboardInterrupt, GeneratorExit, CustomBaseException])
)
def test_timeout_fuzz_base_exceptions(exc_class: type[BaseException]):
    """
    Fuzz the timeout decorator with uncatchable BaseExceptions.

    The timeout decorator uses a background thread. If the thread encounters a
    BaseException, it typically bypasses the standard `except Exception` block,
    causing the thread to die without populating the result or exception lists.
    This test ensures the hardened decorator gracefully handles these cases by
    returning a RuntimeError instead of throwing an unhandled IndexError.
    """

    @timeout(1.0, use_signal=False)
    def target_function() -> None:
        raise exc_class("Fuzzing exception")

    with pytest.raises(
        RuntimeError,
        match="Thread execution failed without returning a result or exception in target_function",
    ):
        target_function()
