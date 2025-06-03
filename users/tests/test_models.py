from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_image_default(self):
        self.assertFalse(bool(self.user.image))