class AuthenticationError(Exception):
    """Raised when the user is not authenticated."""
    pass

class AuthorizationError(Exception):
    """Raised when the user does not have the necessary permissions."""
    pass

class NotFoundError(Exception):
    """Raised whenn entity was not found in database."""
    pass


class EmailAlreadyExists(Exception):
    """Raised when new user tries to be created with existing email."""
    pass