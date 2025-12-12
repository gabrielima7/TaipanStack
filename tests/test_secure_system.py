"""Tests for the secure_system module."""

import logging
from uuid import uuid4

import pytest
from pydantic import SecretStr, ValidationError

from app.secure_system import (
    InMemoryUserRepository,
    UserCreate,
    UserNotFoundError,
    UserService,
)


def test_create_user_success(caplog: pytest.LogCaptureFixture) -> None:
    """Test creating a user with valid data."""
    repository = InMemoryUserRepository()
    service = UserService(repository)
    user_create = UserCreate(
        username="valid_user",
        email="user@example.com",
        password=SecretStr("secure_password"),
        ip_address="192.168.1.1",
    )

    with caplog.at_level(logging.INFO):
        user = service.create_user(user_create)

    assert user.username == "valid_user"
    assert user.email == "user@example.com"
    assert user.is_active is True
    assert service.get_user(user.id) == user

    assert f"User created with ID: {user.id}" in caplog.text


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


def test_get_non_existent_user(caplog: pytest.LogCaptureFixture) -> None:
    """Test retrieving a non-existent user raises UserNotFoundError."""
    repository = InMemoryUserRepository()
    service = UserService(repository)
    user_id = uuid4()
    with caplog.at_level(logging.WARNING):
        with pytest.raises(UserNotFoundError) as exc_info:
            service.get_user(user_id)

    assert str(user_id) in str(exc_info.value)
    assert f"User not found: {user_id}" in caplog.text
