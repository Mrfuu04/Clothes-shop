from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket

@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения успешно внесены!')
        else:
            errors = [error for error in form.errors.values()]
            messages.error(request, *errors)

    context = {
        'title': 'Profile',
        'form': UserProfileForm(instance=request.user),
        'basket': Basket.objects.filter(user=request.user)
    }

    return render(request, 'authapp/profile.html', context=context)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('mainapp:index'))
            else:
                print('User inactive')
        else:
            print(form.errors)
    else:
        form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form,
    }

    return render(request, 'authapp/login.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(request, 'authapp/register.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))
