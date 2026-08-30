from uuid import uuid4

from src.app.secure_system import InMemoryUserRepository, UserInDB

from taipanstack.core.result import Err, Ok


def test_secure_system_update_user():
    repo = InMemoryUserRepository()
    user_id = uuid4()
    user1 = UserInDB(
        id=user_id,
        username="testuser",
        email="test@example.com",
        password_hash="hash",
        is_active=True,
        is_superuser=False,
    )
    repo.save(user1)

    # create second user
    user2 = UserInDB(
        id=uuid4(),
        username="testuser2",
        email="test2@example.com",
        password_hash="hash",
        is_active=True,
        is_superuser=False,
    )
    repo.save(user2)

    # update user1 with new email
    user1_updated = UserInDB(
        id=user_id,
        username="testuser_updated",
        email="test_updated@example.com",
        password_hash="hash",
        is_active=True,
        is_superuser=False,
    )
    res = repo.save(user1_updated)
    assert isinstance(res, Ok)

    # update user1 with existing email of user2
    user1_conflict = UserInDB(
        id=user_id,
        username="testuser_conflict",
        email="test2@example.com",
        password_hash="hash",
        is_active=True,
        is_superuser=False,
    )
    res = repo.save(user1_conflict)
    assert isinstance(res, Err)

    # update user1 with existing username of user2
    user1_conflict2 = UserInDB(
        id=user_id,
        username="testuser2",
        email="test_free@example.com",
        password_hash="hash",
        is_active=True,
        is_superuser=False,
    )
    res = repo.save(user1_conflict2)
    assert isinstance(res, Err)
