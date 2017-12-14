from timemanager.views.user_api import DAO as user_dao
import json


user_skull = {
    'username': 'admin',
    'full_name': 'a user',
    'email': 'admin1@gmail.com',
    'password': 'normal',
    'is_admin': False,
    'is_manager': False,
    'pref_wh': 3,
}


def create_users():
    user1 = user_skull.copy()
    user1['username'] = 'admin1'
    user1['email'] = 'admin1@gmail.com'
    user_dao.create(user1)

    user2 = user_skull.copy()
    user2['username'] = 'admin2'
    user2['email'] = 'admin2@gmail.com'
    user_dao.create(user2)

    user3 = user_skull.copy()
    user3['username'] = 'man1'
    user3['email'] = 'man1@gmail.com'
    user_dao.create(user3)

    user4 = user_skull.copy()
    user4['username'] = 'man2'
    user4['email'] = 'man2@gmail.com'
    user_dao.create(user4)

    user5 = user_skull.copy()
    user5['username'] = 'normal1'
    user5['email'] = 'normal1@gmail.com'
    user_dao.create(user5)

    user6 = user_skull.copy()
    user6['username'] = 'normal2'
    user6['email'] = 'normal2@gmail.com'
    user_dao.create(user6)


def login(interface, email, password):
    resp = interface.app.post(
        'api/v1/auth/login',
        data=json.dumps({
            'email': email,
            'password': password
        }),
        headers={'content-type': 'application/json'},
        follow_redirects=True
    )
    data = json.loads(resp.data.decode('utf-8'))
    interface.assertEqual(resp.status_code, 200)
    return data['token']

