"""Tests for the secure_system module."""

from typing import Optional
from uuid import UUID, uuid4

import pytest
from pydantic import SecretStr, ValidationError

from app.secure_system import (
    User,
    UserCreate,
    UserNotFoundError,
    UserRepository,
    UserService,
)


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository for testing."""

    def __init__(self) -> None:
        """Initialize the in-memory repository."""
        self._storage: dict[UUID, User] = {}

    def save(self, user: User) -> None:
        """Save a user to the in-memory storage."""
        self._storage[user.id] = user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user from the in-memory storage."""
        return self._storage.get(user_id)


def test_create_user_success() -> None:
    """Test creating a user with valid data."""
    repository = InMemoryUserRepository()
    service = UserService(repository)
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
    """Test retrieving a non-existent user raises UserNotFoundError."""
    repository = InMemoryUserRepository()
    service = UserService(repository)
    user_id = uuid4()
    with pytest.raises(UserNotFoundError) as exc_info:
        service.get_user(user_id)
    assert str(user_id) in str(exc_info.value)
