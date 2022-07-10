from django.core.management.base import BaseCommand
import json

from authapp.models import User
from mainapp.models import ProductCategory, Products


def read_json(file_path):
    with open(f'mainapp/fixtures/{file_path}', 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    """
    Заполняет БД данными из ../fixtures/productcategory.json и ../fixtures/products.json,
    Создает суперпользователя name=root password=123
    """

    def handle(self, *args, **options):
        ProductCategory.objects.all().delete()
        categories = read_json('productcategory.json')

        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            ProductCategory(**cat).save()

        Products.objects.all().delete()
        products = read_json('products.json')

        for product in products:
            prod = product.get('fields')
            cat = prod.get('category')
            _cat_id = ProductCategory.objects.get(id=cat)
            prod['category'] = _cat_id
            Products(**prod).save()

        User.objects.create_superuser('root', email=None, password='123')
