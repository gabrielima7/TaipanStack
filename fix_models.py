with open("tests/test_config_models_operations_expected.py", "r") as f:
    content = f.read()

content = content.replace("""def test_config_models_invalid_python_version_too_old_expected() -> None:
    \"\"\"Test that a Python version older than supported is rejected.\"\"\"
    import pytest

    from taipanstack.config.models import StackConfig

    with pytest.raises(ValidationError) as exc_info:
        StackConfig(python_version="3.9")

    assert "not supported" in str(exc_info.value)
""", "")

content = content.replace(
"""        assert config.security.level == "paranoid"
        assert config.logging.level == "DEBUG"
""",
"""        assert config.security.level == "paranoid"
        assert config.logging.level == "DEBUG"

    def test_config_models_invalid_python_version_too_old_expected(self) -> None:
        \"\"\"Test that a Python version older than supported is rejected.\"\"\"
        with pytest.raises(ValidationError) as exc_info:
            StackConfig(python_version="3.9")

        assert "not supported" in str(exc_info.value)
"""
)
with open("tests/test_config_models_operations_expected.py", "w") as f:
    f.write(content)
