import hashlib, uuid
import jwt
from timemanager import app
from timemanager.models.user_model import User


def hash_password(password, salt=None):
    """
    hashes password
    https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
    """
    if salt is None:
        salt = uuid.uuid4().hex.encode('utf-8')
    else:
        salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    # need to encode unicode
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password, salt


def generate_token(user):
    secret = app.config['SECRET_KEY']
    encoded = jwt.encode({'id': user.id, 'email': user.email}, secret, algorithm='HS256')
    return encoded.decode('utf-8')


def decode_token(token):
    secret = app.config['SECRET_KEY']
    data = jwt.decode(token, secret, algorithms=['HS256'])
    user = User.query.get(data['id'])
    return user
