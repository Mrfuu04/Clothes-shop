from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'adminapp/admin.html')


def admin_show_users(request):
    pass


def admin_create_user(request):
    pass


def admin_delete_user(request):
    pass


def admin_update_user(request):
    pass
