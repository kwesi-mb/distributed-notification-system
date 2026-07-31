class UserException(Exception):
    """Base exception for all user-related errors."""

    def __init__(self, message: str = "User service error"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(UserException):
    """Raised when a user cannot be found."""

    def __init__(self, message: str = "User not found"):
        super().__init__(message)

class UserAlreadyExistsException(UserException):
    """Raised when attempting to create or update a user with an email that already exists."""

    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message)

class InvalidCredentialsException(UserException):
    """Raised when login credentials are invalid"""

    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message)

class UserDisabledException(UserException):
    """Raised when a disabled account attempts to authenticate."""

    def __init__(self, message: str = "User account is disabled"):
        super().__init__(message)

class InvalidPasswordException(UserException):
    """Raised when the supplied password does not meet requirements."""

    def __init__(self, message: str = "Invalid password"):
        super().__init__(message)

class DuplicatePushTokenException(UserException):
    """Raised when a push token is already assigned to another user."""

    def __init__(self, message: str = "Push token already exists"):
        super().__init__(message)

    