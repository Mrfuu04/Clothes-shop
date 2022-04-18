from django.db import models


# Create your models here.

class ProductCategory(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    class Meta:
        verbose_name_plural = 'Products'

    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.category}'
