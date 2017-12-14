from tests import TimeManagerTestCase
from tests.utils import login, send_get_request, create_task


class TestTaskRead(TimeManagerTestCase):
    def test_user_can_read_own(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        self.assertIn('70', resp.data.decode('utf-8'))
        resp = send_get_request(self, 'api/v1/tasks/1', token=token)
        self.assertIn('normal', resp.data.decode('utf-8'))

    def test_admin_can_read_normals_task(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        token = login(self, 'admin1@gmail.com', 'password')
        resp = send_get_request(self, 'api/v1/tasks/1', token=token)
        self.assertIn('normal', resp.data.decode('utf-8'))

    def test_admin_can_read_mans_task(self):
        token = login(self, 'man3@gmail.com', 'password')
        resp = create_task(self, token, msg='man')
        token = login(self, 'admin1@gmail.com', 'password')
        resp = send_get_request(self, 'api/v1/tasks/1', token=token)
        self.assertIn('man', resp.data.decode('utf-8'))

    def test_man_cannot_read_other_task(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        token = login(self, 'man3@gmail.com', 'password')
        resp = send_get_request(self, 'api/v1/tasks/1', token=token)
        self.assertNotIn('normal', resp.data.decode('utf-8'))

    def test_anon_cannot_read_any_task(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        resp = send_get_request(self, 'api/v1/tasks/1')
        self.assertNotIn('normal', resp.data.decode('utf-8'))

    def test_admin_can_read_own(self):
        token = login(self, 'admin1@gmail.com', 'password')
        resp = create_task(self, token, msg='admin')
        self.assertIn('70', resp.data.decode('utf-8'))
        resp = send_get_request(self, 'api/v1/tasks/1', token=token)
        self.assertIn('admin', resp.data.decode('utf-8'))

    def test_man_can_read_own(self):
        token = login(self, 'man3@gmail.com', 'password')
        resp = create_task(self, token, msg='man')
        self.assertIn('70', resp.data.decode('utf-8'))
        resp = send_get_request(self, 'api/v1/tasks/1', token=token)
        self.assertIn('man', resp.data.decode('utf-8'))
