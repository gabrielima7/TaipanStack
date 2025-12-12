"""Tests for the secure_system module."""

from uuid import uuid4

import pytest
from pydantic import SecretStr, ValidationError

from app.secure_system import UserCreate, UserService


def test_create_user_success() -> None:
    """Test creating a user with valid data."""
    service = UserService()
    user_create = UserCreate(
        username="valid_user",
        email="user@example.com",
        password=SecretStr("secure_password"),
        ip_address="192.168.1.1",
    )

    user = service.create_user(user_create)

    assert user.username == "valid_user"
    assert user.email == "user@example.com"
    assert user.is_active is True
    assert service.get_user(user.id) == user


def test_create_user_invalid_email() -> None:
    """Test creating a user with an invalid email raises ValidationError."""
    with pytest.raises(ValidationError):
        UserCreate(
            username="valid_user",
            email="invalid-email",
            password=SecretStr("secure_password"),
        )


def test_create_user_invalid_username() -> None:
    """Test creating a user with an invalid username raises ValidationError."""
    with pytest.raises(ValidationError):
        UserCreate(
            username="invalid user name",  # Spaces not allowed
            email="user@example.com",
            password=SecretStr("secure_password"),
        )


def test_get_non_existent_user() -> None:
    """Test retrieving a non-existent user returns None."""
    service = UserService()
    assert service.get_user(uuid4()) is None
