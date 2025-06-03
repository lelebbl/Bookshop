from django.test import TestCase
from main.models import Category, Product
from django.urls import reverse

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Jewellery", slug="jewellery")

    def test_str(self):
        self.assertEqual(str(self.category), "Jewellery")

    def test_get_absolute_url(self):
        # get_absolute_url для перехода на список товаров по категории
        url = reverse('main:product_list_by_category', args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), url)

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Clothes", slug="clothes")
        self.product = Product.objects.create(
            category=self.category,
            name="Jumper",
            slug="jumper",
            price=500.00,
            discount=0,
            available=True
        )
        self.discounted = Product.objects.create(
            category=self.category,
            name="Shirt",
            slug="shirt",
            price=800.00,
            discount=25,
            available=True
        )

    def test_str(self):
        self.assertEqual(str(self.product), "Jumper")

    def test_get_absolute_url(self):
        # get_absolute_url ведёт на detail-страницу товара
        url = reverse('main:product_detail', args=[self.product.slug])
        self.assertEqual(self.product.get_absolute_url(), url)

    def test_sell_price_without_discount(self):
        self.assertEqual(self.product.sell_price(), 500.00)

    def test_sell_price_with_discount(self):
        expected = round(800.00 - 800.00 * 25 / 100, 2)
        self.assertEqual(self.discounted.sell_price(), expected)