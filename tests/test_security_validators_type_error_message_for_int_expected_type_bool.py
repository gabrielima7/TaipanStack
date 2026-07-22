def test_security_validators_type_error_message_for_int_expected_type_bool() -> None:
    import pytest

    from taipanstack.security.validators import _validate_type

    with pytest.raises(TypeError, match="Value must be int, got bool"):
        _validate_type(True, int, "Value")
