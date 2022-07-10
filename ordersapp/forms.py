from django import forms

from mainapp.models import Products
from ordersapp.models import Order, OrderItem

class OrderForm(forms.ModelForm):
    """Форма заказа"""
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields:
            field.widget.attrs['class'] = 'form-contorl'


class OrderItemForm(forms.ModelForm):
    """Форма отдельного товара в заказе"""
    price = forms.CharField(label='Цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Products.get_items().select_related()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
