from flask_restplus import Namespace, Resource, fields
from flask_login import login_required, current_user

from timemanager.models.user_model import User as UserModel  # noqa

from timemanager.helpers.dao import BaseDAO
from timemanager.helpers.database import save_to_db
from timemanager.helpers.auth import hash_password
from timemanager.helpers.errors import ValidationError
from timemanager.helpers.utils import AUTH_HEADER_DEFN
from timemanager.helpers.permissions import has_user_access, staff_only


api = Namespace('users', description='Users', path='/')  # noqa

USER = api.model('User', {
    'id': fields.Integer(required=True),
    'email': fields.String(required=True),
    'username': fields.String(required=True),
    'pref_wh': fields.Float(),
    'full_name': fields.String(),
})

USER_COMPLETE = api.clone('UserFull', USER, {
    'is_admin': fields.Boolean(required=True),
    'is_manager': fields.Boolean(required=True)
})

USER_POST = api.clone('UserPost', USER, {
    'password': fields.String(required=True),
})
del USER_POST['id']

USER_PUT = api.clone('UserPut', USER_POST)


class UserDAO(BaseDAO):
    def create(self, data):
        # validate
        data = self.validate(data)
        # gen phash
        phash, salt = hash_password(data['password'])
        del data['password']
        data['phash'] = phash
        data['salt'] = salt.decode('utf-8')
        # save to database
        user = self.model(**data)
        if not save_to_db(user):
            raise ValidationError('email', 'The username or email already exists')
        # return token at login
        return self.get(user.id), 201

DAO = UserDAO(UserModel, USER_POST, USER_PUT)


@api.route('/users/<int:user_id>')
class User(Resource):
    @login_required
    @has_user_access
    @api.header(*AUTH_HEADER_DEFN)
    @api.doc('get_user')
    @api.marshal_with(USER)
    def get(self, user_id):
        """Fetch a user given its id"""
        return DAO.get(user_id)

    @login_required
    @has_user_access
    @api.header(*AUTH_HEADER_DEFN)
    @api.doc('update_user')
    @api.marshal_with(USER)
    @api.expect(USER_PUT)
    def put(self, user_id):
        """Update a user given its id"""
        return DAO.update(user_id, self.api.payload)


@api.header(*AUTH_HEADER_DEFN)
@api.route('/users/user')
class UserCurrent(Resource):
    @login_required
    @api.doc('get_user_current')
    @api.marshal_with(USER)
    def get(self):
        """Fetch the current user"""
        return DAO.get(current_user.id)


@api.route('/users')
class UserList(Resource):
    @api.doc('create_user')
    @api.marshal_with(USER)
    @api.expect(USER_POST)
    def post(self):
        """Create an user"""
        return DAO.create(self.api.payload)

    @api.header(*AUTH_HEADER_DEFN)
    @login_required
    @staff_only
    @api.doc('list_users')
    @api.marshal_list_with(USER_COMPLETE)
    def get(self):
        """List all users"""
        # TODO: make it admin only
        # also think about levels
        return DAO.list()
