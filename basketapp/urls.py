from django.urls import path

from basketapp.views import BasketAdd, BasketUpdate, BasketRemove


app_name = 'basketapp'
urlpatterns = [
    path('basket_add/<int:product_id>', BasketAdd.as_view(), name='basket_add'),
    path('basket_remove/<int:basket_id>', BasketRemove.as_view(), name='basket_remove'),
    path('edit/<int:basket_id>/<int:quantity>/',
         BasketUpdate.as_view(), name='basket_edit')
]
