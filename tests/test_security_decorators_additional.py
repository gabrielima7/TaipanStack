import pytest


def test_security_decorators_additional_security_decorators_validate_inputs_return_value():
    from taipanstack.security.decorators import validate_inputs

    def my_validator(x):
        return x * 2

    @validate_inputs(x=my_validator)
    def my_func(x):
        return x

    assert my_func(x=5) == 10


def test_security_decorators_additional_security_decorators_guard_exceptions_log_errors():
    from unittest.mock import patch

    from taipanstack.security.decorators import guard_exceptions

    @guard_exceptions(log_errors=True, default=0)
    def my_func():
        raise ValueError("mocked error")

    with patch("logging.getLogger") as mock_get_logger:
        assert my_func() == 0
        mock_get_logger.return_value.warning.assert_called()


def test_security_decorators_additional_security_decorators_require_type_missing_param():
    from taipanstack.security.decorators import require_type

    @require_type(x=int)
    def my_func(y):
        return y

    assert my_func(y=1) == 1


def test_security_decorators_additional_security_decorators_require_type_exception():
    from taipanstack.security.decorators import require_type

    @require_type(x=int)
    def my_func(x):
        return x

    with pytest.raises(TypeError):
        my_func(x="string")


def test_security_decorators_additional_security_decorators_validate_inputs_missing_param():
    from taipanstack.security.decorators import validate_inputs

    def my_validator(x):
        return x * 2

    @validate_inputs(x=my_validator)
    def my_func(y):
        return y

    assert my_func(y=5) == 5


def test_security_decorators_additional_security_decorators_validate_inputs_no_return():
    from taipanstack.security.decorators import validate_inputs

    def my_validator(x):
        return None

    @validate_inputs(x=my_validator)
    def my_func(x):
        return x

    assert my_func(x=5) == 5


def test_security_decorators_additional_security_decorators_guard_exceptions_log_errors_false():
    from taipanstack.security.decorators import guard_exceptions

    @guard_exceptions(log_errors=False, default=0)
    def my_func():
        raise ValueError("mocked error")

    assert my_func() == 0


def test_security_decorators_additional_security_decorators_timeout_exception():

    from taipanstack.security.decorators import timeout

    @timeout(0.01, use_signal=False)
    def my_func():
        raise ValueError("mocked error")

    with pytest.raises(ValueError, match="mocked error"):
        my_func()


def test_security_decorators_additional_security_decorators_guard_exceptions_reraise():
    from taipanstack.security.decorators import guard_exceptions
    from taipanstack.security.guards import SecurityError

    @guard_exceptions(reraise_as=SecurityError)
    def my_func():
        raise ValueError("mocked error")

    with pytest.raises(SecurityError, match="mocked error"):
        my_func()

    @guard_exceptions(reraise_as=RuntimeError)
    def my_func2():
        raise ValueError("mocked error")

    with pytest.raises(RuntimeError, match="mocked error"):
        my_func2()


def test_security_decorators_additional_security_decorators_validate_inputs_validation_error():
    from taipanstack.security.decorators import ValidationError, validate_inputs

    def my_validator(x):
        raise ValueError("validation failed")

    @validate_inputs(x=my_validator)
    def my_func(x):
        return x

    with pytest.raises(ValidationError):
        my_func(x=5)


def test_security_decorators_additional_security_decorators_timeout_thread_success():

    from taipanstack.security.decorators import timeout

    @timeout(1.0, use_signal=False)
    def my_func():
        return 42

    assert my_func() == 42


def test_security_decorators_additional_security_decorators_timeout_thread_exception():

    from taipanstack.security.decorators import timeout

    @timeout(1.0, use_signal=False)
    def my_func():
        raise ValueError("mocked error")

    with pytest.raises(ValueError, match="mocked error"):
        my_func()


def test_security_decorators_additional_security_decorators_timeout_signal_success():
    from taipanstack.security.decorators import timeout

    @timeout(1.0, use_signal=True)
    def my_func():
        return 42

    assert my_func() == 42


def test_security_decorators_additional_security_decorators_timeout_signal_timeout():
    import time

    from taipanstack.security.decorators import OperationTimeoutError, timeout

    @timeout(0.01, use_signal=True)
    def my_func():
        time.sleep(0.05)
        return 42

    with pytest.raises(OperationTimeoutError):
        my_func()


def test_security_decorators_additional_security_decorators_deprecated():

    from taipanstack.security.decorators import deprecated

    @deprecated(removal_version="2.0", message="Use new_func instead")
    def my_func():
        return 42

    with pytest.warns(
        DeprecationWarning,
        match="my_func is deprecated. Will be removed in version 2.0. Use new_func instead",
    ):
        assert my_func() == 42


def test_security_decorators_additional_security_decorators_timeout_invalid_timeout():
    from taipanstack.security.decorators import timeout

    with pytest.raises(ValueError, match="timeout must be a finite"):

        @timeout(-1.0)
        def my_func():
            return 0


def test_security_decorators_additional_security_decorators_deprecated_no_version_no_message():

    from taipanstack.security.decorators import deprecated

    @deprecated()
    def my_func():
        return 42

    with pytest.warns(DeprecationWarning, match="my_func is deprecated."):
        assert my_func() == 42


def test_security_decorators_additional_security_decorators_require_type_correct_type():
    from taipanstack.security.decorators import require_type

    @require_type(x=int)
    def my_func(x):
        return x

    assert my_func(x=42) == 42


def test_security_decorators_additional_security_decorators_timeout_thread_timeout():
    import time

    from taipanstack.security.decorators import OperationTimeoutError, timeout

    @timeout(0.01, use_signal=False)
    def my_func():
        time.sleep(0.05)
        return 42

    with pytest.raises(OperationTimeoutError):
        my_func()
