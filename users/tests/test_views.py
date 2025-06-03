from django.test import TestCase
from django.urls import reverse
from users.models import User


class UserViewsTest(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'pass12345'}
        self.user = User.objects.create_user(**self.credentials)

    def test_login_view_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post(self):
        response = self.client.post(reverse('users:login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('users:logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_register_view_get(self):
        response = self.client.get(reverse('users:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html') 

    def test_register_view_post(self):
        response = self.client.post(reverse('users:registration'), {
            'username': 'newbie',
            'email': 'newbie@mail.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }, follow=True)
        self.assertTrue(User.objects.filter(username='newbie').exists())

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_profile_view_authenticated(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')