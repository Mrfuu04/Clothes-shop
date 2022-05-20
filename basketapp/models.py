from django.db import models

# Create your models here.
from authapp.models import User
from mainapp.models import Products


class BasketQuerySet(models.QuerySet):
        
    def delete(self, *args, **kwargs):
        if kwargs.get('key') != 'make_order':
            for object in self:
                object.product.quantity += object.quantity
                object.product.save()
        super(BasketQuerySet, self).delete()

class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

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

    def delete(self, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super(Basket, self).delete(**kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            item = self._get_item_quantity(self.pk)
            self.product.quantity -= self.quantity - item
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(Basket, self).save(*args, **kwargs)

    @staticmethod
    def _get_item_quantity(pk):
        return Basket.objects.get(pk=pk).quantity
