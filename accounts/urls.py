from django.urls import path
from . import views

app_name = 'accounts_ext'

urlpatterns = [
    path('org', views.create_organisation, name='org_create'),
]
