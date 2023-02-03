# Django
from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm
)

# Local
from auths.models import Client


class ClientCreationForm(UserCreationForm):

    class Meta:
        model = Client
        fields = (
            'email',
        )


class ClientChangeForm(UserChangeForm):

    class Meta:
        model = Client
        fields = (
            'email',
        )


class ClientForm(forms.ModelForm):
    email = forms.EmailField(
        label='Почта'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль'
    )

    class Meta:
        model = Client
        fields = (
            'email',
            'password',
        )
