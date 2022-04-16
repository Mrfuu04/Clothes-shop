from django.urls import path

from adminapp.views import index, admin_show_users, admin_create_user, admin_delete_user, admin_update_user

app_name = 'adminapp'
urlpatterns = [
    path('', index, name='index'),
    path('users/', admin_show_users, name='users'),
    path('user_create/', admin_create_user, name='user_create'),
    path('user_delete/<int:id>', admin_delete_user, name='user_delete'),
    path('user_update/<int:id>', admin_update_user, name='user_update'),
]