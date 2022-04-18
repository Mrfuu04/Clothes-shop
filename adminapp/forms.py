from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm

from authapp.models import User
from mainapp.models import ProductCategory


class UserAdminRegisterForm(UserCreationForm):
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

    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AdminCategoryChange, self).__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'





