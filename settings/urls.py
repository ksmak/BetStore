# Django
from django.conf import settings
from django.contrib import admin
from django.urls import (
    include,
    path
)

# First party
from main.views import simple


urlpatterns = [
    path('admin/', admin.site.urls),
    path('simple/', simple),
    path('', include('main.urls')),
]
                     

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]