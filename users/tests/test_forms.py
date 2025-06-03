from django.test import TestCase
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from users.models import User


class UserFormsTest(TestCase):
    def test_login_form_valid(self):
        User.objects.create_user(username='john', password='pass')
        form = UserLoginForm(data={'username': 'john', 'password': 'pass'})
        self.assertTrue(form.is_valid())


    def test_registration_form_valid(self):
        form = UserRegistrationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_profile_form(self):
        user = User.objects.create_user(username='profileuser')
        form = ProfileForm(instance=user, data={'username': 'updated'})
        self.assertTrue(form.is_valid())