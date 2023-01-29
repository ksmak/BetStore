# Django
from django.urls import (
    path,
    re_path
)

# Local
from .views import (
    IndexView,
    simple
)


urlpatterns = [
    path('', IndexView.as_view(), name='page_main'),
    path('simple/', simple, name='page_simple')
]