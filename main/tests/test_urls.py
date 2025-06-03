from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main import views

class MainUrlsTest(SimpleTestCase):
    def test_popular_list_url(self):
        path = reverse('main:popular_list')
        self.assertEqual(path, '/')
        self.assertEqual(resolve(path).func, views.popular_list)

    def test_product_list_url(self):
        path = reverse('main:product_list')
        self.assertEqual(path, '/shop/')
        self.assertEqual(resolve(path).func, views.product_list)

    def test_product_list_by_category_url(self):
        path = reverse('main:product_list_by_category', args=['test'])
        self.assertEqual(path, '/shop/category/test/')
        self.assertEqual(resolve(path).func, views.product_list)

    def test_product_detail_url(self):
        path = reverse('main:product_detail', args=['item'])
        self.assertEqual(path, '/shop/item/')
        self.assertEqual(resolve(path).func, views.product_detail)
