from tests import TimeManagerTestCase
from tests.utils import login, create_task, send_put_request


class TestTaskUpdate(TimeManagerTestCase):
    def update_task(self, task_id, data, token=None):
        return send_put_request(self, 'api/v1/tasks/' + str(task_id), data, token=token)

    def test_user_can_update_own(self):
        token = login(self, 'normal5@gmail.com', 'password')
        create_task(self, token, msg='normal')
        resp = self.update_task(1, {'title': 'toptal'}, token=token)
        self.assertIn('toptal', resp.data.decode('utf-8'))

    def test_admin_can_update_own(self):
        token = login(self, 'admin1@gmail.com', 'password')
        create_task(self, token, msg='admin')
        resp = self.update_task(1, {'title': 'toptal'}, token=token)
        self.assertIn('toptal', resp.data.decode('utf-8'))

    def test_man_can_update_own(self):
        token = login(self, 'man3@gmail.com', 'password')
        create_task(self, token, msg='manager')
        resp = self.update_task(1, {'title': 'toptal'}, token=token)
        self.assertIn('toptal', resp.data.decode('utf-8'))

    def test_admin_can_update_normals_task(self):
        token = login(self, 'normal5@gmail.com', 'password')
        create_task(self, token, msg='normal')
        # update
        token = login(self, 'admin1@gmail.com', 'password')
        resp = self.update_task(1, {'title': 'toptal'}, token=token)
        self.assertIn('toptal', resp.data.decode('utf-8'))

    def test_admin_can_update_managers_task(self):
        token = login(self, 'man3@gmail.com', 'password')
        create_task(self, token, msg='manager')
        # update
        token = login(self, 'admin1@gmail.com', 'password')
        resp = self.update_task(1, {'title': 'toptal'}, token=token)
        self.assertIn('toptal', resp.data.decode('utf-8'))

    def test_manager_cannot_update_others_task(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='manager', user_id=6)
        # update fail
        token = login(self, 'man3@gmail.com', 'password')
        resp = self.update_task(1, {'title': 'toptal'}, token=token)
        self.assertEqual(resp.status_code, 403)  # unauthorized

    def test_user_cannot_update_others_task(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='manager', user_id=6)
        # update fail
        token = login(self, 'normal6@gmail.com', 'password')
        resp = self.update_task(1, {'title': 'toptal'}, token=token)
        self.assertEqual(resp.status_code, 403)  # unauthorized

