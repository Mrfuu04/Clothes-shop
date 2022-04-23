from django import template

from mainapp.models import ProductCategory, Products

register = template.Library()


@register.simple_tag()
def get_all_categories():
    return ProductCategory.objects.all()


@register.simple_tag()
def get_all_products():
    return Products.objects.all()