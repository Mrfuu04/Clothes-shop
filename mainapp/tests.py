from django.test import TestCase

# Create your tests here.
from authapp.models import User
from mainapp.models import ProductCategory, Products
from django.test.client import Client


class TestProductsSmoke(TestCase):

    def setUp(self) -> None:
        self.category = ProductCategory.objects.create(name='Категория')
        self.good_1 = Products.objects.create(name=f'good 1', category=self.category)
        self.good_2 = Products.objects.create(name=f'good 2', category=self.category)

        self.client = Client()
        self.user = User.objects.create_superuser(username='root', password='123')

    def test_products(self):
        for i in range(3, 10):
            product = Products.objects.create(name=f'Продукт {i}', category=self.category)
            response = self.client.get(f'/detail/{i}/')
            self.assertEqual(response.status_code, 200)

    def test_model_products(self):
        good_1 = Products.objects.get(name='good 1')
        self.assertEqual(good_1, self.good_1)

        good_2 = Products.objects.get(name='good 2')
        self.assertEqual(str(good_2), 'good 2 | Категория')

        self.assertEqual(list(good_2.get_items()), [good_1, good_2])


    def test_auth(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username='root', password='123')
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
