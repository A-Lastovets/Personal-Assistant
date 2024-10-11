from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логін',
        })
    )

    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )

    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        })
    )

    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Підтвердження пароля',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логін',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        })
    )

    class Meta:
        model = Profile
        fields = ['avatar']
