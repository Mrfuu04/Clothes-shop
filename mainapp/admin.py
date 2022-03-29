from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategory, Products

admin.site.register(ProductCategory)
admin.site.register(Products)
