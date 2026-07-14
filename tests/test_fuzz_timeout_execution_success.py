import pytest

from taipanstack.security.decorators import timeout


class CustomBaseException(BaseException): ...


@pytest.mark.parametrize(
    "exc_class", [SystemExit, KeyboardInterrupt, GeneratorExit, CustomBaseException]
)
def test_fuzz_timeout_timeout_fuzz_base_exceptions_execution_success(
    exc_class: type[BaseException],
):
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

    with pytest.raises(exc_class, match="Fuzzing exception"):
        target_function()
