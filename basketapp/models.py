from django.db import models

# Create your models here.
from authapp.models import User
from mainapp.models import Products


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина {self.user.username}'


    def get_sum(self):
        return self.quantity * self.product.price

    def get_result_sum(self):
        basket = Basket.objects.filter(user=self.user)
        return sum(good.get_sum() for good in basket)

    def get_quantity(self):
        basket = Basket.objects.filter(user=self.user)
        return sum(good.quantity for good in basket)
