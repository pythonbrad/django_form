from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('', views.index, name='about'),
    path('', views.index, name='getting-started'),
    path('forms', views.forms, name='forms'),
]
