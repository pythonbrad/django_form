from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('forms', views.forms, name='forms'),
    path('form/new', views.new_form, name='new_form'),
    path('form/<int:pk>/edit', views.edit_form, name='edit_form'),
    path('form/<int:pk>/delete', views.delete_form, name='delete_form'),
    path('form/<int:pk>/entries', views.entries, name='entries'),
    path('form/<int:pk>/entry/new', views.new_entry, name='new_entry'),
    path('form/entry/<int:pk>/edit', views.edit_entry, name='edit_entry'),
    path('form/entry/<int:pk>/delete', views.delete_entry, name='delete_entry'),
    path('form/<int:pk>/records', views.records, name='records'),
    path('form/<code>', views.new_record, name='new_record'),
]
