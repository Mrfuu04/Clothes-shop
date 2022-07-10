from django.conf import settings
from django.core.cache import cache

from mainapp.models import Products, ProductCategory


def get_links_menu_category(cat_slug):
    """Возвращает ссылки на товары по слагу"""
    if settings.LOW_CACHE:
        key = 'category_products'
        category_product = cache.get(key)
        if category_product is None:
            category_product = Products.objects.filter(category__slug=cat_slug).select_related('category')
            cache.set(key, category_product)
        return category_product
    else:
        return Products.objects.filter(category__slug=cat_slug).select_related('category')

def get_links_menu():
    """Возвращает все ссылки на товары"""
    if settings.LOW_CACHE:
        key = 'all_products'
        all_products = cache.get(key)
        if all_products is None:
            all_products = Products.objects.all()
            cache.set(key, all_products)
        return all_products
    return Products.objects.all()


def get_categories():
    """Возвращает все категории"""
    if settings.LOW_CACHE:
        key = 'all_cats'
        all_cats = cache.get(key)
        if all_cats is None:
            all_cats = ProductCategory.objects.all()
            cache.set(key, all_cats)
        return all_cats
    return ProductCategory.objects.all()
