# Future
from __future__ import annotations

# Python
from typing import Any

# Django
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import (
    HttpResponse,
    HttpRequest,
)
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password

# Local
from auths.models import Client
from .models import Event
from auths.forms import ClientForm


def simple(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        '<h1>Что нибудь</h1>'
    )


class IndexView(View):
    """IndexView."""

    queryset: QuerySet = \
        Event.objects.all()
    
    template_name: str = 'main/index.html'

    def get(
        self,
        request: WSGIRequest,
        *args: Any,
        **kwargs: Any
    ) -> HttpResponse:
        """GET request handler."""
        
        form: ClientForm = ClientForm()

        return render(
            request=request,
            template_name=self.template_name,
            context={
                'ctx_form': form,
                'ctx_title': 'Ставки на спорт!',
                'ctx_events': self.queryset,
            }
        )

    def post(
        self,
        request: WSGIRequest,
        *args: Any,
        **kwargs: Any
    ) -> HttpResponse:
        """POST request handler."""
        
        form: ClientForm = ClientForm(
            request.POST
        )

        if form.is_valid():
            user: Client = form.save(
                commit=False
            )

            user.password = make_password(
                user.password
            )

            user.save()
            
            login(
                request=request,
                user=user
            )
        
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'ctx_form': form,
                'ctx_title': 'Ставки на спорт!',
                'ctx_events': self.queryset,
            }
        )

        