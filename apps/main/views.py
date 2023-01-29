# Future
from __future__ import annotations

# Python
from typing import Any

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse
from django.template import (
    backends,
    loader
)
from django.views import View

# Local
from .models import Event


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

        ctx_data: dict[str, str | list[int]] = {
            'ctx_title': 'Заголовок главной страницы',
            'ctx_events': self.queryset
        }

        template: backends.django.Template =\
            loader.get_template(
                self.template_name
            )
        return HttpResponse(
            template.render(
                ctx_data,
                request
            ),
            content_type='text/html'
        )