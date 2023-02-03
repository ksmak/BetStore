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
    # return render(
    #     request,
    #     template_name='main/simple.html',
    #     context={}
    # )


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

        ctx_data: dict[str, Any] = {
            'ctx_title': '(4) Ставки на спорт!',
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