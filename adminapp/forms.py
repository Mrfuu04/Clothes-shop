from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm

from authapp.models import User
from mainapp.models import ProductCategory, Products


class UserAdminRegisterForm(UserCreationForm):
    """Форма создания пользователя через кастомную админку"""
    avatar = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['avatar'].widget.attrs['class'] = 'custom_file-input'


    def clean_password2(self):
        pass



class AdminUserChange(UserChangeForm):
    """Форма изменения пользователя через кастомную админку"""
    avatar = forms.ImageField(widget=forms.FileInput, required=False)
    age = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'age', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AdminUserChange, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['age'].widget.attrs['color'] = 'red'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['avatar'].widget.attrs['class'] = 'custom_file-input'


class AdminCategoryChange(ModelForm):
    """Форма создания и изменения категории через кастомную админку"""

    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AdminCategoryChange, self).__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class AdminProductCreate(ModelForm):
    """Форма создания и изменения товара через кастомную админку"""

    class Meta:
        model = Products
        fields = ('name', 'image', 'description', 'price', 'quantity', 'category', 'is_active')

    def __init__(self, *args, **kwars):
        super(AdminProductCreate, self).__init__(*args, **kwars)


        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'

        self.fields['image'].widget.attrs['class'] = 'custom_file-input'
