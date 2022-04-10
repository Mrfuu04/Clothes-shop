from django.urls import path

from basketapp.views import basket_add, basket_edit, basket_remove


app_name = 'basketapp'
urlpatterns = [
    path('basket_add/<int:id>', basket_add, name='basket_add'),
    path('basket_remove/<int:basket_id>', basket_remove, name='basket_remove'),
    path('edit/<int:basket_id>/<int:quantity>/',
         basket_edit, name='basket_edit')
]
