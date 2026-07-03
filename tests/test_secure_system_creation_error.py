
from src.app.secure_system import (
    InMemoryUserRepository,
    UserCreate,
    UserCreationError,
    UserService,
)

from taipanstack.core.result import Err


def test_secure_system_creation_error_standard_expected():
    repo = InMemoryUserRepository()
    service = UserService(repo)
    user_data = UserCreate(
        username="user_large_pwd",
        email="large@example.com",
        password="a" * 2000
    )
    result = service.create_user(user_data)
    assert isinstance(result, Err)
    assert isinstance(result.err_value, UserCreationError)
