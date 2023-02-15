class BackendError(Exception):
    ...


class AuthenticationException(BackendError):
    ...


class AuthorizationException(AuthenticationException):
    ...
