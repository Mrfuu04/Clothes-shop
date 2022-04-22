from django.urls import path

from adminapp.views import AdminIndexView, AdminShowUsersView, AdminCreateUserView, AdminUserDeleteView, AdminUserUpdateView, \
    AdminCategoryView, \
    AdminCategoryUpdateView, AdminCategoryDeleteView, AdminCategoryCreateView, AdminProductsShowView, \
    AdminProductCreateView, AdminProductChangeView, AdminProductDeleteView

app_name = 'adminapp'
urlpatterns = [
    path('', AdminIndexView.as_view(), name='index'),
    path('users/', AdminShowUsersView.as_view(), name='users'),
    path('user_create/', AdminCreateUserView.as_view(), name='user_create'),
    path('user_delete/<int:pk>/', AdminUserDeleteView.as_view(), name='user_delete'),
    path('user_update/<int:pk>/', AdminUserUpdateView.as_view(), name='user_update'),
    path('categories/', AdminCategoryView.as_view(), name='categories'),
    path('category_update/<int:pk>/', AdminCategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', AdminCategoryDeleteView.as_view(), name='category_delete'),
    path('category_create/', AdminCategoryCreateView.as_view(), name='category_create'),
    path('admin_products/', AdminProductsShowView.as_view(), name='admin_products_show'),
    path('admin_product_create/', AdminProductCreateView.as_view(), name='admin_product_create'),
    path('admin_product_update/<int:pk>/', AdminProductChangeView.as_view(), name='admin_product_update'),
    path('admin_product_delete/<int:pk>/', AdminProductDeleteView.as_view(), name='admin_product_delete'),
]