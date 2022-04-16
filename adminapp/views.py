from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from adminapp.forms import UserAdminRegisterForm, AdminUserChange
from authapp.models import User


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def index(request):
    context = {
        'title': 'GeekShop | Админка'
    }
    return render(request, 'adminapp/admin.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_show_users(request):
    context = {
        'title': 'Список пользователей',
        'users': User.objects.all()
    }

    return render(request, 'adminapp/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_create_user(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
        else:
            print(form.errors)
    else:
        form = UserAdminRegisterForm()

    context = {
        'title': 'Создание пользователя',
        'form': form
    }

    return render(request, 'adminapp/admin-users-create.html', context=context)


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_update_user(request, id):
    if request.method == 'POST':
        form = AdminUserChange(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        else:
            errors = [error for error in form.errors.values()]
            messages.error(request, *errors)

    context = {
        'title': 'Профиль',
        'id': id,
        'form': AdminUserChange(instance=request.user),
    }

    return render(request, 'adminapp/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_delete_user(request, id):
    user_select = User.objects.get(id=id)
    user_select.is_active = False
    user_select.save()

    return HttpResponseRedirect(reverse('adminapp:users'))
