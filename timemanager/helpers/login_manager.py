from flask_login import LoginManager
from flask import g

from timemanager import app
from timemanager.helpers.errors import NotAuthorizedError
from timemanager.models.user_model import User
from timemanager.helpers.auth import decode_token

# Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.header_loader
def load_user_from_header(header_val):
    header_val = header_val.replace('Bearer ', '', 1)
    user = decode_token(header_val)
    # set user status
    g.is_admin = user.is_admin
    g.is_manager = user.is_manager
    # return the user
    return user


@login_manager.unauthorized_handler
def unauthorized():
    raise NotAuthorizedError('Token not set or it is incorrect')
