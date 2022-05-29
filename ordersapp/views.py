from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from adminapp.mixin import AuthorisationDispatchMixin
from mainapp.models import Products
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from basketapp.models import Basket


class OrdersListView(ListView, AuthorisationDispatchMixin):
    template_name = 'ordersapp/orders_list.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(CreateView):
    model = Order
    success_url = reverse_lazy('ordersapp:order_create')
    template_name = 'ordersapp/order_create.html'
    fields = []

    def get_context_data(self, **kwargs):
        data = super(OrderCreateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user).select_related('user')
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitem'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ordersitems = context['orderitem']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if ordersitems.is_valid():
                ordersitems.instance = self.object
                ordersitems.save()

        if self.object.total_cost() == 0:
            self.object.delete()

        return super(OrderCreateView, self).form_valid(form)


@login_required(login_url='/login')
def make_order(request):
    """Функция для добавления заказа в список заказов при нажатии на кнопку 'Оформить'"""
    baskets = Basket.objects.filter(user=request.user)
    order = Order(user=request.user)
    order.save()
    for good in baskets:
        OrderItem.objects.create(order=order, product=good.product, quantity=good.quantity)
    baskets.delete(key='make_order')

    return HttpResponseRedirect(reverse('ordersapp:orders'))


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'ordersapp/order_create.html'
    success_url = reverse_lazy('ordersapp:orders')
    fields = []

    def get_context_data(self, **kwargs):
        data = super(OrderUpdateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                             extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for num, form in enumerate(formset.forms):
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        data['orderitem'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitem']

        with transaction.atomic():
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.total_cost() == 0:
                self.object.delete()
        return super(OrderUpdateView, self).form_valid(form)


class OrderReadView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderReadView, self).get_context_data(**kwargs)
        context['title'] = 'Заказ'
        return context


def order_forming_complete(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:orders'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Products.objects.get(pk=pk)
        if product:
            return JsonResponse({'price': product.price})
        return JsonResponse({'price': 0})
