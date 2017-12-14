from tests import TimeManagerTestCase
from tests.utils import login


class TestUserRead(TimeManagerTestCase):
    def test_nothing(self):
        login(self, 'admin1@gmail.com', 'normal')
