"""Tests for secure models."""

import json

import pytest
from pydantic import BaseModel, SecretStr

from taipanstack.security.models import SecureBaseModel
from taipanstack.utils.logging import REDACTED_VALUE


class TestSecureBaseModel:
    """Tests for the SecureBaseModel."""

    def test_model_dump_masks_sensitive_fields(self) -> None:
        """Test that model_dump redacts sensitive keys."""

        class User(SecureBaseModel):
            username: str
            password: str
            secret_token: str
            api_key: SecretStr

        user = User(
            username="testuser",
            password="supersecretpassword",
            secret_token="tok_12345",
            api_key=SecretStr("real_api_key"),
        )

        dumped = user.model_dump()
        assert dumped["username"] == "testuser"
        assert dumped["password"] == REDACTED_VALUE
        assert dumped["secret_token"] == REDACTED_VALUE
        assert dumped["api_key"] == REDACTED_VALUE

    def test_model_dump_json_masks_sensitive_fields(self) -> None:
        """Test that model_dump_json redacts sensitive keys."""

        class Config(SecureBaseModel):
            app_name: str
            db_password: str

        config = Config(app_name="MyApp", db_password="db_secret_pass")
        json_str = config.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["app_name"] == "MyApp"
        assert parsed["db_password"] == REDACTED_VALUE

    def test_nested_masking(self) -> None:
        """Test masking works on nested models."""

        class DbConfig(BaseModel):
            password: str
            port: int

        class AppConfig(SecureBaseModel):
            debug: bool
            db: list[DbConfig]

        config = AppConfig(
            debug=True,
            db=[
                DbConfig(password="pass1", port=5432),
                DbConfig(password="pass2", port=5433),
            ],
        )

        dumped = config.model_dump()
        assert dumped["debug"] is True
        assert dumped["db"][0]["port"] == 5432
        assert dumped["db"][0]["password"] == REDACTED_VALUE
        assert dumped["db"][1]["password"] == REDACTED_VALUE

    def test_model_dump_json_with_indent(self) -> None:
        """Test model_dump_json with indent."""

        class ApiKeyObj(SecureBaseModel):
            api_key: str

        obj = ApiKeyObj(api_key="123")
        json_str = obj.model_dump_json(indent=2)
        assert "{\n" in json_str
        assert REDACTED_VALUE in json_str

    def test_masking_disabled_when_no_regex(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that data is returned verbatim when no regex is active."""
        from taipanstack.security import models

        monkeypatch.setattr(models, "_SENSITIVE_KEY_REGEX", None)

        class SimpleModel(SecureBaseModel):
            password: str

        obj = SimpleModel(password="will_not_be_masked")
        dumped = obj.model_dump()
        assert dumped["password"] == "will_not_be_masked"
