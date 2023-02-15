from functools import wraps
from flask_jwt_extended import current_user, verify_jwt_in_request
from application.services.exceptions import AuthenticationException, AuthorizationException


def user_logged_in(require_claims=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as err:
                raise AuthenticationException(
                    f"You need to login in order to perform this action. Error: {err}") from err

            if require_claims:
                if require_claims not in current_user.permissions:
                    raise AuthorizationException("You are unauthorised to perform the action.")

            return f(*args, **kwargs)

        return decorated
    return decorator


class UserPrincipal:
    def __init__(self, email, permissions, is_super_admin, login):
        self.email = email
        self.permissions = permissions
        self.is_super_admin = is_super_admin
        self.login = login
