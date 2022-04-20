from django.urls import path
from mainapp.views import index, products

app_name = 'mainapp'
urlpatterns = [
    path('', index, name='index'),
    path('products/', products, name='products'),
    path('category_id/<int:category_id>/', products, name='category_id'),
    path('page/<int:page>/', products, name='page'),
]