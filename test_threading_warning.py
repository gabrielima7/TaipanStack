import pytest
import warnings
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
    @timeout(1.0, use_signal=False)
    def target_function() -> None:
        raise exc_class("Fuzzing exception")

    # If the thread dies of an uncatchable exception, we expect a RuntimeError
    with pytest.raises(
        RuntimeError,
        match="Thread execution failed without returning a result or exception in target_function",
    ):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", pytest.PytestUnhandledThreadExceptionWarning)
            target_function()
