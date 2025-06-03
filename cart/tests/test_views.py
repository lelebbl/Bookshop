from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from main.models import Category, Product
from cart.cart import Cart


class CartViewsTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="C", slug="c")
        self.product = Product.objects.create(
            category=self.cat,
            name="P",
            slug="p",
            price=50.00,
            discount=0,
            available=True
        )

    def test_cart_add_view(self):
        url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(url, {'quantity': 2, 'override': False})
        # Должен перенаправить на detail корзины
        self.assertRedirects(response, reverse('cart:cart_detail'))
        # В сессии должна быть запись о добавленном товаре
        session = self.client.session
        key = settings.CART_SESSION_ID
        self.assertIn(str(self.product.id), session[key])

    def test_cart_remove_view(self):
        # Сразу помещаем товар в сессию
        session = self.client.session
        session[settings.CART_SESSION_ID] = {
            str(self.product.id): {
                'quantity': 1,
                'price': str(self.product.price),
                'product_id': self.product.id  # Сохраняем только ID продукта и другие данные
            }
        }
        session.save()
        url = reverse('cart:cart_remove', args=[self.product.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('cart:cart_detail'))
        # Товара больше нет в корзине
        session = self.client.session
        self.assertNotIn(str(self.product.id), session.get(settings.CART_SESSION_ID, {}))

    def test_cart_detail_view(self):
        url = reverse('cart:cart_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        # Контекст должен содержать объект Cart
        self.assertIsInstance(response.context['cart'], Cart)