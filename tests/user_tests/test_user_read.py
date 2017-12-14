from tests import TimeManagerTestCase
from tests.utils import login, send_get_request


class TestUserReadPositive(TimeManagerTestCase):
    def test_normal_can_read_own(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/5')
        self.assertIn('normal5', resp.data.decode('utf-8'))

    def test_manager_can_read_own(self):
        token = login(self, 'man3@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/3')
        self.assertIn('man3', resp.data.decode('utf-8'))

    def test_admin_can_read_own(self):
        token = login(self, 'admin1@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/1')
        self.assertIn('admin1', resp.data.decode('utf-8'))

    def test_admin_can_read_normal(self):
        token = login(self, 'admin1@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/5')
        self.assertIn('normal5', resp.data.decode('utf-8'))

    def test_admin_can_read_man(self):
        token = login(self, 'admin1@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/4')
        self.assertIn('man4', resp.data.decode('utf-8'))

    def test_man_can_read_normal(self):
        token = login(self, 'man3@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/6')
        self.assertIn('normal6', resp.data.decode('utf-8'))


class TestUserReadNegative(TimeManagerTestCase):
    def test_normal_cannot_read_other_normal(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/6')
        self.assertNotIn('normal6', resp.data.decode('utf-8'))

    def test_normal_cannot_read_man(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/3')
        self.assertNotIn('man3', resp.data.decode('utf-8'))

    def test_normal_cannot_read_admin(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/1')
        self.assertNotIn('admin1', resp.data.decode('utf-8'))

    def test_man_cannot_read_other_man(self):
        token = login(self, 'man3@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/4')
        self.assertNotIn('man4', resp.data.decode('utf-8'))

    def test_man_cannot_read_admin(self):
        token = login(self, 'man3@gmail.com', 'password')
        resp = send_get_request(self, token, 'api/v1/users/1')
        self.assertNotIn('admin1', resp.data.decode('utf-8'))
