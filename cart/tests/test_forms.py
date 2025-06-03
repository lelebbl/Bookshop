from django.test import TestCase
from cart.forms import CartAddProductForm


class CartFormTest(TestCase):
    def test_valid_form(self):
        data = {'quantity': 3, 'override': False}
        form = CartAddProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_quantity(self):
        # Количество вне разрешенного диапазона (1-10)
        data = {'quantity': 0, 'override': False}
        form = CartAddProductForm(data=data)
        self.assertFalse(form.is_valid())