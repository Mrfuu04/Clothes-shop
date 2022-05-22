from django.urls import path

from ordersapp.views import OrdersListView, OrderCreateView, OrderDeleteView, \
    OrderUpdateView, OrderReadView, make_order, order_forming_complete, get_product_price

app_name = 'ordersapp'
urlpatterns = [
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('order_update/<int:pk>', OrderUpdateView.as_view(), name='order_update'),
    path('order_read/<int:pk>', OrderReadView.as_view(), name='order_read'),
    path('make_order/', make_order, name='make_order'),
    path('purchase/<int:pk>/', order_forming_complete, name='purchase'),
    path('product/<int:pk>/', get_product_price, name='product_price'),
]
