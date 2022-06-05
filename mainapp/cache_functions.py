from django.conf import settings
from django.core.cache import cache

from mainapp.models import Products


def get_links_menu(category_id):
    if settings.LOW_CACHE:
        key = 'category_products'
        category_product = cache.get(key)
        if category_product is None:
            key = Products.objects.filter(category=category_id).select_related('category')
            cache.set(key, category_product)
        return category_product
    else:
        return Products.objects.filter(category=category_id).select_related('category')


def get_product_detail(pk):
    if settings.LOW_CACHE:
        key = 'product'
        product = cache.get(key)
        if product is None:
            key = Products.objects.filter(pk=pk).select_related('category')
            cache.set(key, product)
        return product
    else:
        return Products.objects.filter(pk=pk)
