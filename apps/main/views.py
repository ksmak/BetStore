# Future
from __future__ import annotations

# Python
from typing import Any

# Django
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
)
from django.template import (
    backends,
    loader
)
from django.views import View

# Local
from .models import Event
from auths.forms import ClientForm

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
        form: ClientForm = ClientForm()

        ctx_data: dict[str, Any] = {
            'ctx_form': form,
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
            form.save()
        
        return HttpResponseRedirect('/')
        