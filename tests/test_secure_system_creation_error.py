from src.app.secure_system import (
    InMemoryUserRepository,
    UserCreate,
    UserCreationError,
    UserService,
)

from taipanstack.core.result import Err


def test_secure_system_creation_error_secure_system_creation_error():
    repo = InMemoryUserRepository()
    service = UserService(repo)

    # Test length exceeded
    user_data = UserCreate(
        username="user_large_pwd", email="large@example.com", password="a" * 2000
    )
    result = service.create_user(user_data)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, UserCreationError)

    # Test empty password
    user_data_empty = UserCreate(
        username="user_empty_pwd", email="empty@example.com", password=""
    )
    result_empty = service.create_user(user_data_empty)
    assert isinstance(result_empty, Err)
    assert isinstance(result_empty.err_value, UserCreationError)
