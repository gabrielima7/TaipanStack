"""
Secure System Module.

This module demonstrates a secure implementation of a user management service
following strict typing and security guidelines.
"""

import threading
from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from pydantic import EmailStr, Field, SecretStr
from pydantic.networks import IPvAnyAddress

from taipanstack.core.result import Err, Ok, Result
from taipanstack.security import SecureBaseModel, hash_password
from taipanstack.utils.logging import get_logger

# Configure logger
logger = get_logger(__name__)


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: UUID) -> None:
        """Initialize the exception with the user ID."""
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found.")


class UserAlreadyExistsError(Exception):
    """Exception raised when a user already exists."""

    def __init__(self, message: str) -> None:
        """Initialize the exception with a message."""
        self.message = message
        super().__init__(message)


class UserCreationError(Exception):
    """Exception class for user creation errors."""

    def __init__(self, message: str = "Failed to create user") -> None:
        """Initialize the exception with a message."""
        self.message = message
        super().__init__(message)


class UserCreate(SecureBaseModel):
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
    ip_address: IPvAnyAddress | None = None


class User(SecureBaseModel):
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


class UserInDB(User):
    """
    Model representing a registered user in the database.

    Attributes:
        password_hash: The hashed password of the user.

    """

    password_hash: str


class UserRepository(ABC):
    """Abstract base class for user data access."""

    @abstractmethod
    def save(self, user: UserInDB) -> Result[None, UserAlreadyExistsError]:
        """
        Save a user to the repository.

        Args:
            user: The user to save.

        """

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> UserInDB | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The UUID of the user.

        Returns:
            The UserInDB object if found, otherwise None.

        """


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository."""

    def __init__(self) -> None:
        """Initialize the in-memory repository."""
        self._storage: dict[UUID, UserInDB] = {}
        self._lock = threading.Lock()

    def save(self, user: UserInDB) -> Result[None, UserAlreadyExistsError]:
        """
        Save a user to the in-memory storage.

        Args:
            user: The user to save.

        """
        with self._lock:
            if any(
                (u.username == user.username or u.email == user.email) \
                    and u.id != user.id
                for u in self._storage.values()
            ):
                return Err(
                    UserAlreadyExistsError(
                        f"User {user.username} already exists."
                    )
                )
            self._storage[user.id] = user
            return Ok(None)

    def get_by_id(self, user_id: UUID) -> UserInDB | None:
        """
        Retrieve a user from the in-memory storage.

        Args:
            user_id: The UUID of the user.

        Returns:
            The UserInDB object if found, otherwise None.

        """
        with self._lock:
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

    def create_user(self, user_create: UserCreate) -> Result[User, UserCreationError]:
        """
        Create a new user.

        Args:
            user_create: The user creation data.

        Returns:
            Ok(User) on success, Err(UserCreationError) on failure.

        """
        # Hash the password securely using the security module
        pwd_hash = hash_password(user_create.password)

        user_id = uuid4()
        user_in_db = UserInDB(
            id=user_id,
            username=user_create.username,
            email=user_create.email,
            password_hash=pwd_hash,
        )
        save_result = self._user_repository.save(user_in_db)
        match save_result:
            case Ok():
                logger.info("User created successfully", user_id=user_in_db.id)
                # Return the public User model, excluding the password hash
                public_user = User(
                    id=user_in_db.id,
                    username=user_in_db.username,
                    email=user_in_db.email,
                    is_active=user_in_db.is_active,
                )
                return Ok(public_user)
            case Err(error):
                logger.warning("Failed to create user", user_id=user_in_db.id)
                return Err(UserCreationError(message=str(error)))
            case _:
                return Err(UserCreationError(message="Unknown save error"))  # type: ignore[unreachable]

    def get_user(self, user_id: UUID) -> Result[User, UserNotFoundError]:
        """
        Retrieve a user by ID using Result pattern.

        Args:
            user_id: The UUID of the user.

        Returns:
            Ok(User) if found, Err(UserNotFoundError) if not found.

        Example:
            >>> result = service.get_user(some_id)
            >>> if isinstance(result, Ok):
            ...     print(f"Found: {result.unwrap().username}")
            ... else:
            ...     print(f"Not found: {result.unwrap_err().user_id}")

        """
        user_in_db = self._user_repository.get_by_id(user_id)
        if user_in_db is None:
            logger.warning("User lookup failed", user_id=user_id)
            return Err(UserNotFoundError(user_id))

        public_user = User(
            id=user_in_db.id,
            username=user_in_db.username,
            email=user_in_db.email,
            is_active=user_in_db.is_active,
        )
        return Ok(public_user)
