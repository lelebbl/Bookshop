from django.test import TestCase
from django.contrib.auth import get_user_model
from main.models import Product, Category
from orders.models import Order, OrderItem
from decimal import Decimal

class OrderModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.user = get_user_model().objects.create_user(username="testuser", password="pass")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            price=Decimal("100.00"),
            available=True
        )
        self.order = Order.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            city="Test City",
            address="123 Test St",
            postal_code="00000",
            paid=True,
            stripe_id="pi_test_123"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("100.00"),
            quantity=2
        )

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id}")

    def test_order_total_cost(self):
        self.assertEqual(self.order.get_total_cost(), Decimal('200.00'))

    def test_order_stripe_url_test(self):
        with self.settings(STRIPE_SECRET_KEY='sk_test_123'):
            self.assertIn('/test/', self.order.get_stripe_url())
            self.assertIn(self.order.stripe_id, self.order.get_stripe_url())

    def test_orderitem_str(self):
        self.assertEqual(str(self.order_item), str(self.order_item.id))

    def test_orderitem_get_cost(self):
        self.assertEqual(self.order_item.get_cost(), Decimal('200.00'))
