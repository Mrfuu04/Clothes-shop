from django.urls import path

from basketapp.views import basket_add, basket_remove


app_name = 'basketapp'
urlpatterns = [
    path('basket_add/<int:id>', basket_add, name='basket_add'),
    path('basket_remove/<int:basket_id>', basket_remove, name='basket_remove'),
]