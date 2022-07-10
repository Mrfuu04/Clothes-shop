from django import template

from mainapp.cache_functions import get_categories
from mainapp.models import ProductCategory, Products

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Возвращает все категории"""
    return get_categories()


@register.simple_tag()
def get_all_products():
    """Возвращает все товары"""
    return Products.objects.all()