from flask_restplus import Namespace  # Resource, fields,
# from flask_login import login_required, current_user

# from timemanager import db
from timemanager.models.user_model import User as UserModel  # noqa


api = Namespace('users', description='Users', path='/')  # noqa
