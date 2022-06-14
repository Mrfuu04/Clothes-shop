from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategory, Products


class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Products, ProductsAdmin)
