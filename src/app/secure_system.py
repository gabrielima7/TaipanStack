"""
Secure System Module.

This module demonstrates a secure implementation of a user management service
following strict typing and security guidelines.
"""

from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from pydantic.networks import IPvAnyAddress


class UserCreate(BaseModel):
    """
    Model for creating a new user.

    Attributes:
        username: The username of the user.
        email: The email address of the user.
        password: The password of the user (will be treated as a secret).
        ip_address: The IP address from which the user is registering.

    """

    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: SecretStr
    ip_address: Optional[IPvAnyAddress] = None

    model_config = ConfigDict(frozen=True)


class User(BaseModel):
    """
    Model representing a registered user.

    Attributes:
        id: Unique identifier for the user.
        username: The username of the user.
        email: The email address of the user.
        is_active: Whether the user account is active.

    """

    id: UUID
    username: str
    email: EmailStr
    is_active: bool = True

    model_config = ConfigDict(frozen=True)


class UserService:
    """Service for managing users securely."""

    def __init__(self) -> None:
        """Initialize the UserService."""
        self._users: dict[UUID, User] = {}

    def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user_create: The user creation data.

        Returns:
            The created User object.

        """
        # In a real system, we would hash the password here.
        # Since strict typing forbids unused variables, we explicitly acknowledge it.
        _ = user_create.password

        user_id = uuid4()
        user = User(
            id=user_id,
            username=user_create.username,
            email=user_create.email,
            is_active=True,
        )
        self._users[user_id] = user
        return user

    def get_user(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id: The UUID of the user.

        Returns:
            The User object if found, otherwise None.

        """
        return self._users.get(user_id)
