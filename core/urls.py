from django.urls import path
from . import views

from django.core.exceptions import PermissionDenied


def boom403(request):
    raise PermissionDenied("Test 403")


def boom500(request):
    1/0  # force a server error


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("force-500/", views.force_500, name="force-500"),
    path("force-403/", views.force_403, name="force-403"),
]
