from django.test import TestCase
from django.urls import reverse
from main.models import Category, Product
from cart.forms import CartAddProductForm

class PopularListViewTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="TestCat", slug="testcat")
        # создаём 4 доступных товара
        for i in range(4):
            Product.objects.create(
                category=cat,
                name=f"Prod{i}",
                slug=f"prod{i}",
                price=100 * i,
                discount=0,
                available=True
            )

    def test_popular_list_shows_three(self):
        # На главной показываются первые 3 товара
        response = self.client.get(reverse('main:popular_list'))
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(len(products), 3)
        self.assertTemplateUsed(response, 'main/index/index.html')

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="X", slug="x")
        self.product = Product.objects.create(
            category=self.cat,
            name="Unique",
            slug="unique",
            price=123.45,
            discount=0,
            available=True
        )

    def test_product_detail_success(self):
        url = reverse('main:product_detail', args=[self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'].slug, self.product.slug)
        # Форма добавления в корзину должна присутствовать
        self.assertIs(response.context['cart_product_form'], CartAddProductForm)
        self.assertTemplateUsed(response, 'main/product/detail.html')

    def test_product_detail_not_found(self):
        response = self.client.get(reverse('main:product_detail', args=['no-such']))
        self.assertEqual(response.status_code, 404)

class ProductListViewTest(TestCase):
    def setUp(self):
        # две категории и товары
        self.cat1 = Category.objects.create(name="C1", slug="c1")
        self.cat2 = Category.objects.create(name="C2", slug="c2")
        # в каждой по 6 товаров
        for i in range(6):
            Product.objects.create(
                category=self.cat1,
                name=f"A{i}", slug=f"a{i}", price=10, discount=0, available=True
            )
            Product.objects.create(
                category=self.cat2,
                name=f"B{i}", slug=f"b{i}", price=20, discount=0, available=True
            )

    def test_product_list_all(self):
        # Без фильтрации возвращаются все товары и 2 страницs (12 товаров)
        response = self.client.get(reverse('main:product_list'))
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        # Всего создано 12 товаров, пагинация по 10 на страницу
        self.assertEqual(products.paginator.num_pages, 2)
        self.assertEqual(products.paginator.count, 12)
        self.assertTemplateUsed(response, 'main/product/list.html')

    def test_product_list_by_category(self):
        # Фильтрация по категории
        url = reverse('main:product_list_by_category', args=[self.cat1.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'].slug, self.cat1.slug)
        # Должно быть 6 товаров только из cat1
        self.assertEqual(response.context['products'].paginator.count, 6)