from flask_login import LoginManager

from timemanager import app
from timemanager.helpers.errors import NotAuthorizedError
from timemanager.models.user_model import User
from timemanager.helpers.auth import get_user_from_header

# Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.header_loader
def load_user_from_header(header_val):
    return get_user_from_header(header_val)


@login_manager.unauthorized_handler
def unauthorized():
    raise NotAuthorizedError('Token not set or it is incorrect')

