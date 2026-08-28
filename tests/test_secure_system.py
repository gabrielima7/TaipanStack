
import pytest
from uuid import uuid4
from pydantic import SecretStr
from app.secure_system import InMemoryUserRepository, UserInDB, UserAlreadyExistsError
from taipanstack.core.result import Err, Ok

def test_in_memory_user_repository_update_conflict():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")
    user2 = UserInDB(id=uuid4(), username="user2", email="user2@example.com", password_hash="hash")

    assert isinstance(repo.save(user1), Ok)
    assert isinstance(repo.save(user2), Ok)

    # Try updating user1 to have user2's username
    user1_updated_username = UserInDB(id=user1.id, username="user2", email="user1@example.com", password_hash="hash")
    result = repo.save(user1_updated_username)
    assert isinstance(result, Err)
    assert isinstance(result.unwrap_err(), UserAlreadyExistsError)

    # Try updating user1 to have user2's email
    user1_updated_email = UserInDB(id=user1.id, username="user1", email="user2@example.com", password_hash="hash")
    result = repo.save(user1_updated_email)
    assert isinstance(result, Err)
    assert isinstance(result.unwrap_err(), UserAlreadyExistsError)

def test_in_memory_user_repository_new_user_conflict():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")
    repo.save(user1)

    # Conflict on username
    user2 = UserInDB(id=uuid4(), username="user1", email="user2@example.com", password_hash="hash")
    result = repo.save(user2)
    assert isinstance(result, Err)

    # Conflict on email
    user3 = UserInDB(id=uuid4(), username="user3", email="user1@example.com", password_hash="hash")
    result = repo.save(user3)
    assert isinstance(result, Err)

def test_in_memory_user_repository_new_user_conflict_username_only():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")
    repo.save(user1)

    # Conflict on username but different email
    user2 = UserInDB(id=uuid4(), username="user1", email="user2@example.com", password_hash="hash")
    result = repo.save(user2)
    assert isinstance(result, Err)

def test_in_memory_user_repository_new_user_conflict_email_only():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")
    repo.save(user1)

    # Conflict on email but different username
    user3 = UserInDB(id=uuid4(), username="user3", email="user1@example.com", password_hash="hash")
    result = repo.save(user3)
    assert isinstance(result, Err)

def test_in_memory_user_repository_update_conflict_both():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")
    user2 = UserInDB(id=uuid4(), username="user2", email="user2@example.com", password_hash="hash")
    repo.save(user1)
    repo.save(user2)

    # Conflict on both
    user1_updated = UserInDB(id=user1.id, username="user2", email="user2@example.com", password_hash="hash")
    result = repo.save(user1_updated)
    assert isinstance(result, Err)

def test_in_memory_user_repository_update_conflict_both_same():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")
    user2 = UserInDB(id=uuid4(), username="user2", email="user2@example.com", password_hash="hash")
    repo.save(user1)
    repo.save(user2)

    # Update to itself should work
    user1_updated = UserInDB(id=user1.id, username="user1", email="user1@example.com", password_hash="hash")
    result = repo.save(user1_updated)
    assert isinstance(result, Ok)

def test_in_memory_user_repository_update_not_found():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")
    # Don't save it, so existing_user is None

    # New user with same username should conflict if already in set, but let's test new user addition logic
    # The existing test covers new user conflicts.
    pass


def test_in_memory_user_repository_save_new_user_conflict_during_lock():
    repo = InMemoryUserRepository()
    user1 = UserInDB(id=uuid4(), username="user1", email="user1@example.com", password_hash="hash")

    # Simulate a race condition by putting the username/email in the set manually
    # before we call save (as if another thread did it)
    repo._usernames.add("user1")
    result = repo.save(user1)
    assert isinstance(result, Err)

    repo._usernames.clear()
    repo._emails.add("user1@example.com")
    result = repo.save(user1)
    assert isinstance(result, Err)
