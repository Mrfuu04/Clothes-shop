from django.urls import path
from mainapp.views import IndexView, ProductDetail, ProductsView

app_name = 'mainapp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductsView.as_view(), name='products'),
    path('category_id/<int:category>/', ProductsView.as_view(), name='category_id'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
]