"""
Secure System Module.

This module demonstrates a secure implementation of a user management service
following strict typing and security guidelines.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from pydantic.networks import IPvAnyAddress

# Configure logger
logger = logging.getLogger(__name__)


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: UUID) -> None:
        """Initialize the exception with the user ID."""
        super().__init__(f"User with ID {user_id} not found.")


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


class UserRepository(ABC):
    """Abstract base class for user data access."""

    @abstractmethod
    def save(self, user: User) -> None:
        """
        Save a user to the repository.

        Args:
            user: The user to save.

        """

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The UUID of the user.

        Returns:
            The User object if found, otherwise None.

        """


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository."""

    def __init__(self) -> None:
        """Initialize the in-memory repository."""
        self._storage: dict[UUID, User] = {}

    def save(self, user: User) -> None:
        """
        Save a user to the in-memory storage.

        Args:
            user: The user to save.

        """
        self._storage[user.id] = user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user from the in-memory storage.

        Args:
            user_id: The UUID of the user.

        Returns:
            The User object if found, otherwise None.

        """
        return self._storage.get(user_id)


class UserService:
    """Service for managing users securely."""

    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the UserService with a repository.

        Args:
            user_repository: The repository to use for data access.

        """
        self._user_repository = user_repository

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
        self._user_repository.save(user)
        logger.info("User created with ID: %s", user.id)
        return user

    def get_user(self, user_id: UUID) -> User:
        """
        Retrieve a user by ID.

        Args:
            user_id: The UUID of the user.

        Returns:
            The User object.

        Raises:
            UserNotFoundError: If the user is not found.

        """
        user = self._user_repository.get_by_id(user_id)
        if user is None:
            logger.warning("User not found: %s", user_id)
            raise UserNotFoundError(user_id)
        return user
