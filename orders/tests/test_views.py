from django.test import TestCase, Client
from django.urls import reverse
from main.models import Product, Category
from orders.models import Order, OrderItem
from django.contrib.auth import get_user_model


class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')  # <--- Важно!
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=100,
            available=True
        )

    def test_order_create_view_get(self):
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/create.html')  # <--- Исправлено

    def test_order_create_view_post(self):
        session = self.client.session
        session['cart'] = {
            str(self.product.id): {'quantity': 2, 'price': '100'}
        }
        session.save()

        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'address': '123 Test St',
            'postal_code': '12345',
            'city': 'Testville',
            'user': self.user.id
        }

        response = self.client.post(reverse('orders:order_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payment:process'))

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
