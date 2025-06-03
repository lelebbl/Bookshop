from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from orders.forms import OrderCreateForm

class OrderCreateFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='12345',
            first_name='John', last_name='Doe', email='john@example.com'
        )

    def test_initial_data_for_authenticated_user(self):
        request = self.factory.get('/')
        request.user = self.user
        form = OrderCreateForm(request=request)
        self.assertEqual(form.initial['first_name'], 'John')
        self.assertEqual(form.initial['last_name'], 'Doe')
        self.assertEqual(form.initial['email'], 'john@example.com')

    def test_form_save_sets_user(self):
        request = self.factory.post('/')
        request.user = self.user
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Test St',
            'postal_code': '00000',
            'city': 'Test City',
            'user': self.user.id
        }
        form = OrderCreateForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertEqual(order.user, self.user)
