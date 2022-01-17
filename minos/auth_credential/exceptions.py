class CredentialConfigException(Exception):
    """Base Api Gateway Exception."""


class NoTokenException(CredentialConfigException):
    """Exception to be raised when token is not available."""


class ApiGatewayConfigException(CredentialConfigException):
    """Base config exception."""
