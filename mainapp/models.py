from django.db import models


# Create your models here.

class ProductCategory(models.Model):
    """Категория"""
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=64, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name


class Products(models.Model):
    """Товар"""
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кол-во')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return f'{self.name} | {self.category}'

    @staticmethod
    def get_items():
        return Products.objects.filter(is_active=True)
