from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from authapp.models import User
from basketapp.models import Basket
from mainapp.models import Products


def basket_add(request, id):
    product = Products.objects.get(id=id)
    user = request.user
    baskets = Basket.objects.filter(user=user, product=product)

    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


