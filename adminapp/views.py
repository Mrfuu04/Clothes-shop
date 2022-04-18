from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from adminapp.forms import UserAdminRegisterForm, AdminUserChange, AdminCategoryChange
from authapp.models import User
from mainapp.models import ProductCategory


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
    else:
        form = AdminUserChange()

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


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_category_show(request):
    context = {
        'title': 'Категории',
        'categories': ProductCategory.objects.all(),
    }

    return render(request, 'adminapp/admin_category_read.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_category_update(request, id):
    product_cat_select = ProductCategory.objects.get(id=id)
    if request.method == 'POST':
        form = AdminCategoryChange(instance=product_cat_select, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
        else:
            print(form.errors)
    else:
        form = AdminCategoryChange(instance=product_cat_select)

    context = {
        'title': 'Обновление категории',
        'form': form,
        'product_cat_select': product_cat_select
    }
    return render(request, 'adminapp/admin_category_update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_category_delete(request, id):
    category_select = ProductCategory.objects.get(id=id)
    category_select.is_active = False
    category_select.save()

    return HttpResponseRedirect(reverse('adminapp:categories'))



@user_passes_test(lambda u: u.is_superuser, login_url='/login')
def admin_category_create(request):
    if request.method == 'POST':
        form = AdminCategoryChange(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
        else:
            errors = [error for error in form.errors.values()]
            messages.error(request, *errors)
    else:
        form = AdminCategoryChange()

    context = {
        'title': 'Создание категории',
        'form': form,
    }

    return render(request, 'adminapp/admin_category_create.html', context)
