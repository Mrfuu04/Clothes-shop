from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
import hashlib

from authapp.models import User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.md5(str(user.username).encode('utf-8')).hexdigest()
        user.activation_key = hashlib.md5(str(user.email+salt).encode('utf-8')).hexdigest()
        user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError("Почта уже существует!")
        return cleaned_data


    def clean_password2(self):
        pass


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput, required=False)
    age = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'age')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['age'].widget.attrs['color'] = 'red'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-1'
        self.fields['avatar'].widget.attrs['class'] = 'custom_file-input'


    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if len(data) > 15:
            raise ValidationError('Слишком длинная фамилия!')
        return data

    def clean_avatar(self):
        data = self.cleaned_data['avatar']
        if data is None:
            return data
        if data.image.format not in ['JPEG', 'PNG']:
            raise ValidationError('Неверный формат картинки')
        return data

