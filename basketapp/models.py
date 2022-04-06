from django.db import models

# Create your models here.
from authapp.models import User
from mainapp.models import Products


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete='CASCADE')
    product = models.ForeignKey(Products, on_delete='CASCADE')
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина {self.user.username}'
