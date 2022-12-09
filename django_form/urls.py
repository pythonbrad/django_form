from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include('debug_toolbar.urls')),
    ] + urlpatterns
