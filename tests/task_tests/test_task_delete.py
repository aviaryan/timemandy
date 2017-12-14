from tests import TimeManagerTestCase
from tests.utils import login, create_task, send_delete_request, send_get_request


class TestTaskDelete(TimeManagerTestCase):
    def delete_task(self, task_id, token=None):
        return send_delete_request(self, 'api/v1/tasks/' + str(task_id), token=token)

    def check_task_deleted(self, task_id):
        token = login(self, 'admin1@gmail.com', 'password')
        resp = send_get_request(self, 'api/v1/tasks/' + str(task_id), token=token)
        self.assertNotEqual(resp.status_code, 200)

    def test_user_can_delete_own(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        self.assertEqual(resp.status_code, 200)
        resp = self.delete_task(1, token=token)
        self.check_task_deleted(1)

    def test_admin_can_delete_normals_task(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        self.assertEqual(resp.status_code, 200)
        token = login(self, 'admin1@gmail.com', 'password')
        resp = self.delete_task(1, token=token)
        self.check_task_deleted(1)

    def test_admin_can_delete_managers_task(self):
        token = login(self, 'man3@gmail.com', 'password')
        resp = create_task(self, token, msg='manager')
        self.assertEqual(resp.status_code, 200)
        token = login(self, 'admin1@gmail.com', 'password')
        resp = self.delete_task(1, token=token)
        self.check_task_deleted(1)

    def test_manager_cannot_delete_others(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        self.assertEqual(resp.status_code, 200)
        token = login(self, 'man3@gmail.com', 'password')
        resp = self.delete_task(1, token=token)
        self.assertEqual(resp.status_code, 403)

    def test_normal_cannot_delete_others(self):
        token = login(self, 'normal5@gmail.com', 'password')
        resp = create_task(self, token, msg='normal')
        self.assertEqual(resp.status_code, 200)
        token = login(self, 'normal6@gmail.com', 'password')
        resp = self.delete_task(1, token=token)
        self.assertEqual(resp.status_code, 403)
