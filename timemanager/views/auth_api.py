from flask_restplus import Namespace, Resource, fields

from timemanager.models.user_model import User as UserModel

from timemanager.helpers.auth import generate_token, hash_password
from timemanager.helpers.errors import NotAuthorizedError


api = Namespace('auth', description='Auth', path='/')  # noqa

LOGIN = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

LOGIN_RESPONSE = api.model('LoginResp', {
    'token': fields.String(),
})


@api.route('/auth/login')
class Login(Resource):
    @api.doc('login_user')
    @api.marshal_with(LOGIN_RESPONSE)
    @api.expect(LOGIN)
    def post(self):
        """Login a user"""
        data = self.api.payload
        user = UserModel.query.filter_by(email=data['email']).first()
        if user is None:
            raise NotAuthorizedError('Bad login credentials')
        # generate and verify phash
        phash, _ = hash_password(data['password'], salt=user.salt)
        # print(user, user.phash, phash)
        if user.phash is not None and user.phash == phash:
            token = generate_token(user)
            return {'token': token}
        else:
            raise NotAuthorizedError('Bad login credentials')
