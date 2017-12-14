from functools import wraps
from flask_login import current_user
from .errors import PermissionDeniedError
from timemanager.models.user_model import User


def staff_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = current_user
        is_user_valid = user and (user.is_admin or user.is_manager)
        if is_user_valid:
            return func(*args, **kwargs)
        else:
            raise PermissionDeniedError(message='Staff account required to access this feature')
    return wrapper


def has_user_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = current_user
        target_user_id = kwargs.get('user_id')
        if target_user_id is None:
            return func(*args, **kwargs)
        target_user = User.query.get(target_user_id)

        if user.is_admin:  # all good
            return func(*args, **kwargs)
        if user.is_manager and (not current_user.is_manager and not current_user.is_admin):  # manager case
            return func(*args, **kwargs)
        if user.id == target_user.id:
            return func(*args, **kwargs)
        # default
        raise PermissionDeniedError(message='You don\'t have access to this account')
    return wrapper
