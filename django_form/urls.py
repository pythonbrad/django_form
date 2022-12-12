from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include('debug_toolbar.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
