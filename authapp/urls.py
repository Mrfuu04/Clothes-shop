from django.urls import path

from authapp.views import GSloginView, GSRegisterView, GSLogout, ProfileView

app_name = 'authapp'
urlpatterns = [
    path('login/', GSloginView.as_view(), name='login'),
    path('register/', GSRegisterView.as_view(), name='register'),
    path('logout/', GSLogout.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<str:email>/<str:key>', GSRegisterView.verify, name='verify')
]