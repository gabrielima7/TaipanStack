def test_security_validators_type_error_message_for_int_expected_type_bool_standard_expected() -> None:
    from taipanstack.security.validators import _validate_type
    import pytest

    with pytest.raises(TypeError, match="Value must be int, got bool"):
        _validate_type(True, int, "Value")
