from django.urls import path

from adminapp.views import index, admin_show_users, admin_create_user, admin_delete_user, admin_update_user, \
    admin_category_show, admin_category_update, admin_category_delete, admin_category_create, admin_products_show, \
    admin_product_create, admin_product_change, admin_product_delete

app_name = 'adminapp'
urlpatterns = [
    path('', index, name='index'),
    path('users/', admin_show_users, name='users'),
    path('user_create/', admin_create_user, name='user_create'),
    path('user_delete/<int:id>/', admin_delete_user, name='user_delete'),
    path('user_update/<int:id>/', admin_update_user, name='user_update'),
    path('categories/', admin_category_show, name='categories'),
    path('category_update/<int:id>/', admin_category_update, name='category_update'),
    path('category_delete/<int:id>/', admin_category_delete, name='category_delete'),
    path('category_create/', admin_category_create, name='category_create'),
    path('admin_products/', admin_products_show, name='admin_products_show'),
    path('admin_product_create/', admin_product_create, name='admin_product_create'),
    path('admin_product_update/<int:id>/', admin_product_change, name='admin_product_update'),
    path('admin_product_delete/<int:id>/', admin_product_delete, name='admin_product_delete'),
]