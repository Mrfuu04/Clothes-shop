from django.conf import settings
from django.db import models


# Create your models here.
from django.utils.functional import cached_property

from mainapp.models import Products


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    STATUSES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PROCEEDED, 'Обрабатывается'),
        (PAID, 'Оплачен'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(choices=STATUSES, max_length=3, default=FORMING, verbose_name='Статус')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    def delete(self, **kwargs):
        for item in self.orderitem.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        # self.status = self.CANCEL
        self.save()

    @cached_property
    def get_items(self):
        items = self.orderitem.select_related()
        return items

    def get_summary(self):
        items = self.orderitem.select_related()
        return {
            'order_total_quantity': sum(list(map(lambda x: x.quantity, items))),
            'order_total_cost': sum(list(map(lambda x: x.product.price * x.quantity, items)))
        }

    def get_total_quantity(self):
        items = self.get_items
        return sum(list(map(lambda x: x.quantity, items)))

    def total_cost(self):
        items = self.get_items
        return sum(list(map(lambda x: x.product.price * x.quantity, items)))

    def __str__(self):
        return f'Заказ | {self.pk}'


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='orderitem', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кол-во')

    def get_product_cost(self):
        return self.product.price * self.quantity

    def delete(self, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super(OrderItem, self).delete(**kwargs)
        



