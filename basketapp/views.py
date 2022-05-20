from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, FormView, DeleteView

from adminapp.mixin import AuthorisationDispatchMixin
from authapp.models import User
from basketapp.models import Basket
from mainapp.models import Products
from django.template.loader import render_to_string


class BasketAdd(CreateView, AuthorisationDispatchMixin):

    def get(self, request, *args, **kwargs):
        id_product = self.kwargs.get('product_id')
        user = self.request.user
        product = Products.objects.get(id=id_product)
        baskets = Basket.objects.filter(user=user, product=product)
        if baskets:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(user=user, product=product, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required(login_url='/login')
# def basket_add(request, id):
#     product = Products.objects.get(id=id)
#     user = request.user
#     baskets = Basket.objects.filter(user=user, product=product)
#
#     if baskets:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#     else:
#         Basket.objects.create(user=user, product=product, quantity=1)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class BasketRemove(DeleteView, AuthorisationDispatchMixin):

    def get(self, request, *args, **kwargs):
        Basket.objects.get(id=self.kwargs.get('basket_id')).delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


# @login_required(login_url='/login')
# def basket_remove(request, basket_id):
#     Basket.objects.get(id=basket_id).delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class BasketUpdate(UpdateView, AuthorisationDispatchMixin):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            basket = Basket.objects.get(id=self.kwargs.get('basket_id'))
            quantity = self.kwargs.get('quantity')
            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()

            baskets = Basket.objects.filter(user=request.user)
            context = {'basket': baskets}

            result = render_to_string(
                'basket_includes/basket_include_ajax.html', context=context)
            return JsonResponse({'result': result})

# def basket_edit(request, basket_id, quantity):
#     if request.is_ajax():
#         basket = Basket.objects.get(id=basket_id)
#         if quantity > 0:
#             basket.quantity = quantity
#             basket.save()
#         else:
#             basket.delete()
#
#         baskets = Basket.objects.filter(user=request.user)
#         context = {'basket': baskets}
#
#         result = render_to_string(
#             'basket_includes/basket_include_ajax.html', context=context)
#         return JsonResponse({'result': result})
