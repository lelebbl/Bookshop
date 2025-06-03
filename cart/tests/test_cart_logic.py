from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from main.models import Category, Product
from cart.cart import Cart


class CartLogicTest(TestCase):
    def setUp(self):
        # Подготовим request с сессией
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(self.request)
        self.request.session.save()

        # Создаём категорию и товар
        self.category = Category.objects.create(name="TestCat", slug="testcat")
        self.product = Product.objects.create(
            category=self.category,
            name="TestProd",
            slug="testprod",
            price=100.00,
            discount=10,
            available=True
        )

        self.cart = Cart(self.request)

    def test_add_and_len(self):
        # Добавляем товар
        self.cart.add(self.product, quantity=2)
        # Длина корзины (количество позиций) = 2
        self.assertEqual(len(self.cart), 2)
        # В сессии появился ключ для корзины
        key = settings.CART_SESSION_ID
        self.assertIn(str(self.product.id), self.request.session[key])

    def test_override_quantity(self):
        # Override заменяет количество
        self.cart.add(self.product, quantity=2)
        self.cart.add(self.product, quantity=5, override_quantity=True)
        self.assertEqual(len(self.cart), 5)

    def test_remove(self):
        # Удаление товара из корзины
        self.cart.add(self.product, quantity=3)
        self.cart.remove(self.product)
        self.assertEqual(len(self.cart), 0)

    def test_clear(self):
        # Полная очистка корзины
        self.cart.add(self.product)
        self.cart.clear()
        key = settings.CART_SESSION_ID
        self.assertNotIn(key, self.request.session)

    def test_get_total_price(self):
        # Цены учитывают скидку: 100 - 10% = 90
        self.cart.add(self.product, quantity=3)
        total = self.cart.get_total_price()
        self.assertEqual(total, '270.00')

    def test_iter(self):
        # Итерация по корзине выдаёт dict с полным объектом продукта
        self.cart.add(self.product, quantity=1)
        items = list(self.cart)
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item['product'], self.product)
        self.assertEqual(item['quantity'], 1)