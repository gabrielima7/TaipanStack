"""Tests for the secure_system module."""

import logging
from uuid import UUID, uuid4

import pytest
from pydantic import SecretStr, ValidationError

from app.secure_system import (
    InMemoryUserRepository,
    User,
    UserAlreadyExistsError,
    UserCreate,
    UserCreationError,
    UserNotFoundError,
    UserRepository,
    UserService,
)
from taipanstack.core.result import Err, Ok
from taipanstack.security import verify_password


def test_create_user_success(caplog: pytest.LogCaptureFixture) -> None:
    """Test creating a user with valid data."""
    repository = InMemoryUserRepository()
    service = UserService(repository)
    user_create = UserCreate(
        username="valid_user",
        email="user@example.com",
        password=SecretStr("secure_password"),
        ip_address=None,
    )

    with caplog.at_level(logging.INFO):
        result = service.create_user(user_create)

    user = result.unwrap()
    assert user.username == "valid_user"
    assert user.email == "user@example.com"
    assert verify_password("secure_password", user.password_hash)

    # Test get_user with Result pattern
    result_get = service.get_user(user.id)
    match result_get:
        case Ok(found_user):
            assert found_user == user
        case Err():
            pytest.fail("Expected Ok but got Err")

    assert "User created successfully" in caplog.text
    assert f"user_id={user.id}" in caplog.text


def test_create_user_failure(caplog: pytest.LogCaptureFixture) -> None:
    """Test user creation failure handled gracefully."""

    # Mock repository to raise an error
    class FailingRepository(UserRepository):
        def save(self, user: object) -> None:
            raise UserAlreadyExistsError("Database error")

        def get_by_id(self, user_id: UUID) -> None:
            return None

    service = UserService(FailingRepository())
    user_create = UserCreate(
        username="fail_user",
        email="fail@example.com",
        password=SecretStr("password"),
        ip_address=None,
    )

    result = service.create_user(user_create)
    match result:
        case Err(UserCreationError(message=msg)):
            assert "Database error" in msg
        case _:
            pytest.fail("Expected Err(UserCreationError)")


def test_create_user_already_exists(caplog: pytest.LogCaptureFixture) -> None:
    """Test creating a user that already exists raises UserAlreadyExistsError."""

    repository = InMemoryUserRepository()
    service = UserService(repository)

    # First user
    user_create_1 = UserCreate(
        username="existing_user",
        email="existing@example.com",
        password=SecretStr("password"),
        ip_address=None,
    )
    service.create_user(user_create_1)

    # Second user with same username
    user_create_2 = UserCreate(
        username="existing_user",
        email="another@example.com",
        password=SecretStr("password"),
        ip_address=None,
    )

    with caplog.at_level(logging.ERROR):
        result = service.create_user(user_create_2)

    match result:
        case Err(UserCreationError(message=msg)):
            assert "already exists" in msg
        case _:
            pytest.fail("Expected Err(UserCreationError) due to duplicate username")

    assert "Failed to create user" in caplog.text

    # Third user with same email
    user_create_3 = UserCreate(
        username="another_user",
        email="existing@example.com",
        password=SecretStr("password"),
        ip_address=None,
    )

    with caplog.at_level(logging.ERROR):
        result = service.create_user(user_create_3)

    match result:
        case Err(UserCreationError(message=msg)):
            assert "already exists" in msg
        case _:
            pytest.fail("Expected Err(UserCreationError) due to duplicate email")

    # Empty repository loop coverage
    empty_repo = InMemoryUserRepository()
    service_empty = UserService(empty_repo)
    user_create_empty = UserCreate(
        username="first_user",
        email="first@example.com",
        password=SecretStr("password"),
        ip_address=None,
    )
    res = service_empty.create_user(user_create_empty)
    assert res.is_ok()

    # Continue loop after first mismatch
    user_create_mismatch = UserCreate(
        username="first_user",  # match
        email="new@example.com",
        password=SecretStr("password"),
        ip_address=None,
    )
    res_mismatch = service_empty.create_user(user_create_mismatch)
    assert res_mismatch.is_err()

    # We need a scenario where existing_user.username does not match, but existing_user.email does match
    # to hit the fallback of the first branch (if existing_user.username == user.username: False)
    user_create_email_match = UserCreate(
        username="new_user",  # mismatch
        email="first@example.com",  # match
        password=SecretStr("password"),
        ip_address=None,
    )
    res_email_match = service_empty.create_user(user_create_email_match)
    assert res_email_match.is_err()

    # Create another user to have 2 existing users, so that the loop iterates without breaking immediately
    user_create_empty_2 = UserCreate(
        username="second_user",
        email="second@example.com",
        password=SecretStr("password"),
        ip_address=None,
    )
    res_2 = service_empty.create_user(user_create_empty_2)
    assert res_2.is_ok()

    # Now create a user where it doesn't match the first one, but matches the second one
    user_create_match_second = UserCreate(
        username="third_user",
        email="second@example.com",  # Matches the second user's email
        password=SecretStr("password"),
        ip_address=None,
    )
    res_match_second = service_empty.create_user(user_create_match_second)
    assert res_match_second.is_err()


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
    """Test retrieving a non-existent user returns Err with UserNotFoundError."""
    repository = InMemoryUserRepository()
    service = UserService(repository)
    user_id = uuid4()

    with caplog.at_level(logging.WARNING):
        result = service.get_user(user_id)

    # Verify Result is Err
    assert result.is_err()
    match result:
        case Err(error):
            assert isinstance(error, UserNotFoundError)
            assert error.user_id == user_id
        case Ok():
            pytest.fail("Expected Err but got Ok")

    assert "User lookup failed" in caplog.text
    assert f"user_id={user_id}" in caplog.text


def test_models_redaction() -> None:
    """Test that UserCreate and User models redact sensitive fields."""
    user_create = UserCreate(
        username="testuser",
        email="test@example.com",
        password=SecretStr("my_secret_password"),
    )

    dumped_create = user_create.model_dump()
    assert dumped_create["password"] == "***REDACTED***"
    assert "my_secret_password" not in str(dumped_create)

    json_create = user_create.model_dump_json()
    assert "***REDACTED***" in json_create
    assert "my_secret_password" not in json_create

    user = User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        password_hash="some_hashed_value",
    )

    dumped_user = user.model_dump()
    assert dumped_user["password_hash"] == "***REDACTED***"
    assert "some_hashed_value" not in str(dumped_user)

    json_user = user.model_dump_json()
    assert "***REDACTED***" in json_user
    assert "some_hashed_value" not in json_user
