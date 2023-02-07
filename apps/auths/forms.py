# Django
from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm
)
from django.core.exceptions import ValidationError
from django.conf import settings

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

    def clean(self) -> None:
        email: str = self.cleaned_data['email']
                
        # 1
        email_parts: list[str] = email.split('@')
        if len(email_parts) == 2 and email_parts[1] in Client.EMAIL_SERVICES:
            pass
        else:
            self.add_error('email', ValidationError(settings.ERROR_EMAIL_INVALID))
        