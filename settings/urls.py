# Django
from django.conf import settings
from django.contrib import admin
from django.urls import (
    include,
    path
)

# First party
from main.views import (
    index,
    simple,
    get_all_users_view
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('simple', simple),
    path('', index),
    path('users/', get_all_users_view)
]
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
